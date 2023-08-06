from typing import Optional, List, Dict, Any


def aggregation_chart(
    groupby: List[Dict[str, Any]],
    metric: List[Dict[str, Any]],
    title: Optional[str] = None,
    page_size: int = 20,
    show_frequencies: bool = False,
    sort_direction: str = "Descending",
):
    """
    Example for aggregates
    [
        {
            "agg": "category",
            "field": "_cluster_.desc_all-mpnet-base-v2_vector_.kmeans-8",
            "name": "category _cluster_.desc_all-mpnet-base-v2_vector_.kmeans-8",
            "aggType": "groupby",
        },
        {
            "agg": "avg",
            "field": "_sentiment_.desc.cardiffnlp-twitter-roberta-base-sentiment.overall_sentiment_score",
            "name": "avg desc (Sentiment Score)",
            "aggType": "metric",
        },
    ]
    """
    assert sort_direction in {"Descending", "Ascending"}

    for query in groupby:
        query["aggType"] = "groupby"

    for query in metric:
        query["aggType"] = "metric"

    return [
        {
            "type": "appBlock",
            "content": [
                {
                    "type": "datasetAggregation",
                    "attrs": {
                        "aggregates": groupby + metric,
                        "datasetId": "",
                        "displayType": "column",
                        "sortBy": "",
                        "sortDirection": sort_direction,
                        "title": "" if title is None else title,
                        "showFrequencies": show_frequencies,
                        "pageSize": page_size,
                        "timeseries": {},
                    },
                }
            ],
        },
    ]
