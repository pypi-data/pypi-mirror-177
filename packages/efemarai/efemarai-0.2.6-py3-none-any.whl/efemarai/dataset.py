import os
import zipfile
from enum import Enum
from time import sleep

import boto3
from appdirs import user_data_dir
from botocore.errorfactory import ClientError

from efemarai.console import console
from efemarai.job_state import JobState
from efemarai.problem_type import ProblemType


class DatasetFormat(Enum):
    """
    Possible dataset formats.
    """

    COCO = "COCO"
    ImageRegression = "ImageRegression"
    ImageNet = "ImageNet"
    TFRecord = "tfrecord"

    @classmethod
    def has(cls, value):
        try:
            cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls._member_map_.values()))


class DatasetStage(Enum):
    Train = "train"
    Validation = "validation"
    Test = "test"

    @classmethod
    def has(cls, value):
        try:
            cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls._member_map_.values()))


class Dataset:
    """
    Provides dataset related functionality.
    It can be created through the :class:`efemarai.project.Project.create_dataset` method.

    Example:

    .. code-block:: python
        :emphasize-lines: 2,5

        import efemarai as ef
        dataset = ef.Session().project("Name").create_dataset(...)
        # do something else
        dataset.reload()
        if dataset.loading_finished:
            print('Dataset has finished loading')

    Example (2):

    .. code-block:: python

        import efemarai as ef
        project = ef.Session().project("Name")
        dataset = project.dataset("Dataset Name")
        print(f"Classes: {dataset.classes}")

    """

    @staticmethod
    def create(
        project,
        name,
        format,
        stage,
        data_url,
        annotations_url,
        credentials,
        upload,
        num_datapoints,
        mask_generation,
        min_asset_size,
    ):
        """
        Create a dataset. A more convenient way is to use `project.create_model(...)`.
        """
        if name is None or data_url is None:
            return None

        assert DatasetFormat.has(
            format
        ), f"Dataset format '{format}' should be in {DatasetFormat.list()}."

        assert DatasetStage.has(
            stage
        ), f"Dataset stage '{stage}' should be in {DatasetStage.list()}."

        assert mask_generation in (None, "Simple", "Advanced")

        response = project._put(
            f"api/dataset/undefined/{project.id}",
            json={
                "name": name,
                "format": format,
                "stage": stage,
                "data_url": data_url,
                "annotations_url": annotations_url,
                "access_token": credentials,
                "upload": upload,
                "projectId": project.id,
            },
        )
        dataset_id = response["id"]

        if upload:
            endpoint = f"api/dataset/{dataset_id}/upload"
            if annotations_url is not None:
                project._upload(annotations_url, endpoint)
            project._upload(data_url, endpoint)
            project._post(
                endpoint,
                json={
                    "num_samples": num_datapoints,
                    "mask_generation": mask_generation,
                    "min_asset_size": min_asset_size,
                },
            )

        return Dataset(
            project,
            dataset_id,
            name,
            format,
            stage,
            data_url,
            annotations_url,
            "NotStarted",
            [],
        )

    @staticmethod
    def _parse_classes(dataset_classes):
        if dataset_classes == []:
            return []

        max_index = max([c["index"] for c in dataset_classes]) + 1

        classes = [None] * max_index
        for c in dataset_classes:
            classes[c["index"]] = c["name"]

        return classes

    def __init__(
        self,
        project,
        id,
        name,
        format,
        stage,
        data_url,
        annotations_url,
        state,
        classes,
    ):
        self.project = (
            project  #: (:class:`efemarai.project.Project`) Associated project.
        )
        self.id = id
        self.name = name  #: (str) Name of the dataset.
        self.format = format  #: (str) Format of the dataset.
        self.stage = stage  #: (str) Stage of the dataset.
        self.data_url = data_url
        self.annotations_url = annotations_url
        self.state = JobState(state)
        self.message = ""
        self.classes = classes  #: (list [str]) List of names of the classes. `None` is used for those ids that don't have a corresponding name.

    def __repr__(self):
        res = f"{self.__module__}.{self.__class__.__name__}("
        res += f"\n  id={self.id}"
        res += f"\n  name={self.name}"
        res += f"\n  format={self.format}"
        res += f"\n  stage={self.stage}"
        res += f"\n  data_url={self.data_url}"
        res += f"\n  annotations_url={self.annotations_url}"
        res += f"\n  state={self.state}"
        res += f"\n  message={self.message}"
        res += f"\n  classes={self.classes}"
        res += f"\n)"
        return res

    @property
    def loading_finished(self):
        """Returns true if the dataset loading has finished.

        :rtype: bool
        """
        return self.state == JobState.Finished

    @property
    def loading_failed(self):
        """Returns true if the dataset loading has failed.

        :rtype: bool
        """
        return self.state == JobState.Failed

    @property
    def loading(self):
        """Returns true if the is still being loaded - not failed or finished.

        :rtype: bool
        """
        return self.state != JobState.Finished and self.state != JobState.Failed

    def delete(self, delete_dependants=False):
        """
        Deletes the dataset.

        You cannot delete an object that is used in a stress test
        or a baseline (delete those first). This cannot be undone.
        """

        self.project._delete(
            f"api/dataset/{self.id}/{self.project.id}/{delete_dependants}",
        )

    def reload(self):
        """
        Reloads the dataset *in place* from the remote endpoint and return it.

        Returns:
            The updated dataset object.
        """

        endpoint = f"api/dataset/{self.id}"
        dataset_details = self.project._get(endpoint)

        self.name = dataset_details["name"]
        self.format = dataset_details["format"]
        self.stage = dataset_details["stage"]
        self.data_url = dataset_details["data_url"]
        self.annotations_url = dataset_details.get("annotations_url")
        self.state = JobState(dataset_details["states"][-1]["name"])
        self.message = dataset_details["states"][-1]["message"]
        self.classes = self._parse_classes(dataset_details["classes"])

        return self

    def download(
        self,
        num_samples=None,
        dataset_format=None,
        path=None,
        unzip=True,
        ignore_cache=False,
    ):
        """
        Download the dataset locally.

        Args:
            num_samples (int): Number of samples to download. Leave `None` for all.
            dataset_format (str): What format to download the dataset. Currently supported include `COCO`, `YOLO`, `VOC`, `ImageNet`, `CSV`.
            path (str): The path where to download the data.
            unzip (bool): Should the downloaded zip be unzipped.
            ignore_cache (bool): Force regeneration of the dataset by ignoring the cache. May lead to slower subsequent calls.
        """

        if self.loading:
            console.print(":poop: Dataset has not finished loading.", style="red")
            return None

        if path is None:
            path = user_data_dir(appname="efemarai")

        path = os.path.join(path, self.id)

        if dataset_format is None:
            if self.project.problem_type == ProblemType.Classification:
                dataset_format = "imagenet"
            elif self.project.problem_type == ProblemType.ObjectDetection:
                dataset_format = "coco"
            elif self.project.problem_type == ProblemType.InstanceSegmentation:
                dataset_format = "coco"

        if dataset_format is None:
            console.print(":poop: Unsupported problem type.", style="red")
            return None

        if not ignore_cache:
            name = os.path.join(path, f"dataset_{dataset_format}")

            if num_samples:
                name += f"_{num_samples}"

            if os.path.exists(name):
                return name

            name += ".zip"
            if os.path.exists(name + ".zip"):
                return name

        access = self.project._post(
            "api/downloadDataset",
            json={
                "id": self.id,
                "format": dataset_format,
                "num_samples": num_samples,
                "async_download": True,
            },
        )

        s3 = boto3.client(
            "s3",
            aws_access_key_id=access["AccessKeyId"],
            aws_secret_access_key=access["SecretAccessKey"],
            aws_session_token=access["SessionToken"],
            endpoint_url=access["Url"],
        )

        with console.status(f"Preparing '{self.name}' dataset download"):
            while True:
                try:
                    response = s3.head_object(
                        Bucket=access["Bucket"], Key=access["ObjectKey"]
                    )
                    size = response["ContentLength"]
                    break
                except ClientError:
                    sleep(1)

        with self.project._session._progress_bar() as progress:
            task = progress.add_task("Downloading dataset ", total=float(size))

            def callback(num_bytes):
                return progress.advance(task, num_bytes)

            os.makedirs(path, exist_ok=True)
            filename = os.path.join(path, os.path.basename(access["ObjectKey"]))

            s3.download_file(
                access["Bucket"], access["ObjectKey"], filename, Callback=callback
            )

        if unzip:
            with console.status("Unzipping dataset"):
                dirname = os.path.splitext(filename)[0]
                with zipfile.ZipFile(filename, "r") as f:
                    f.extractall(dirname)

                os.remove(filename)

                filename = dirname

        console.print(
            (f":heavy_check_mark: Downloaded '{self.name}' dataset to\n  {filename}"),
            style="green",
        )

        return filename
