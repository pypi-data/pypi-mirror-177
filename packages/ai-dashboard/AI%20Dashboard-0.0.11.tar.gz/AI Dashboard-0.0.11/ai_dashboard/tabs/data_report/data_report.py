import uuid

from typing import Union, Optional, Dict, Any, List

from ai_dashboard.api import endpoints
from ai_dashboard.tabs import abstract_tab
from ai_dashboard.tabs.data_report import constants
from ai_dashboard.tabs.data_report import aggregation_chart
from ai_dashboard.tabs.data_report import metric
from ai_dashboard.tabs.data_report import markdown
from ai_dashboard.tabs.data_report import image


class DataReport(abstract_tab.Tab):
    ID = "REPORT"

    BLANK: Dict[str, Any] = {
        "activeFilterGroup": "",
        "color": None,
        "configuration": {"content": {"type": "doc", "content": []}},
        "name": "",
        "type": ID,
    }

    def __init__(
        self,
        endpoints: endpoints.Endpoints,
        dataset_id: str,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()

        self._endpoints = endpoints
        self.title = title

        if config is not None:
            self._config = config
        else:
            self.reset()

        self.dataset_id = dataset_id

        self.config["colour"] = colour.upper() if colour is not None else colour
        self.config["configuration"]["title"] = title
        self.config["name"] = name

    @classmethod
    def from_text(
        cls,
        text: str,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
    ):
        if colour is not None:
            assert colour in constants.colours
        data_report = cls(title=title)
        data_report.config = {
            "name": name,
            "type": "REPORT",
            "color": colour.upper() if colour is not None else colour,
            "configuration": {
                "title": title,
                "content": {
                    "type": "doc",
                    "content": [
                        {
                            "type": "appBlock",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "attrs": {"textAlign": "left"},
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": text,
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                },
            },
            "activeFilterGroup": "",
        }
        return data_report

    @classmethod
    def from_markdown(
        cls,
        text: str,
        title: str,
        name: Optional[str] = None,
        colour: Optional[str] = None,
    ):
        data_report = cls(title=title)
        md = markdown.MarkDown()
        content = md.parse(text)
        data_report.config = {
            "name": name,
            "type": "REPORT",
            "color": colour.upper() if colour is not None else colour,
            "configuration": {
                "title": title,
                "content": {
                    "type": "doc",
                    "content": content,
                },
            },
            "activeFilterGroup": "",
        }
        return data_report

    def insert_local_medias(self, file_paths: List[str]) -> List[str]:
        presigned_urls = self._endpoints._get_file_upload_urls(
            self.dataset_id,
            files=file_paths,
        )
        urls = []
        for index, file_path in enumerate(file_paths):
            url = presigned_urls["files"][index]["url"]
            upload_url = presigned_urls["files"][index]["upload_url"]
            with open(file_path, "rb") as fn_byte:
                media_content = bytes(fn_byte.read())
            urls.append(url)
            response = self._endpoints._upload_media(
                presigned_url=upload_url,
                media_content=media_content,
            )
            assert response.status_code == 200
        return urls

    def add_markdown(self, text: str):
        md = markdown.MarkDown()
        content = md.parse(text)
        config = self.config["configuration"]
        if "content" not in config:
            self.config["configuration"]["content"] = {
                "type": "doc",
                "content": [],
            }
        self.config["configuration"]["content"]["content"] += content

    def add_aggregation(
        self,
        groupby: List[Dict[str, Any]],
        metric: List[Dict[str, Any]],
        title: Optional[str] = None,
        page_size: int = 20,
        show_frequencies: bool = False,
        sort_direction: str = "Descending",
    ):
        chart = aggregation_chart.aggregation_chart(
            groupby=groupby,
            metric=metric,
            title=title,
            page_size=page_size,
            show_frequencies=show_frequencies,
            sort_direction=sort_direction,
        )
        self.config["configuration"]["content"]["content"] += chart

    def add_metric(
        self,
        query: List[Dict[str, Any]],
        title: Optional[str] = None,
        show_frequencies: bool = False,
        sort_direction: str = "Descending",
    ):
        chart = metric.metric(
            query=query,
            title=title,
            show_frequencies=show_frequencies,
            sort_direction=sort_direction,
        )
        self.config["configuration"]["content"]["content"] += chart

    def add_image(self, image_src: Union[bytes, str]):
        if isinstance(image_src, bytes):
            presigned_urls = self._endpoints._get_file_upload_urls(
                self.dataset_id,
                files=[str(uuid.uuid4())],
            )
            url = presigned_urls["files"][0]["url"]
            upload_url = presigned_urls["files"][0]["upload_url"]
            response = self._endpoints._upload_media(
                presigned_url=upload_url,
                media_content=image_src,
            )
            image_src = url
        else:
            image_src = self.insert_local_medias([image_src])[0]
        chart = image.image(image_src)
        self.config["configuration"]["content"]["content"] += chart
