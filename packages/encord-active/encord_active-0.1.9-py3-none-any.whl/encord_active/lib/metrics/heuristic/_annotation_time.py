from loguru import logger

from encord_active.lib.common.iterator import Iterator
from encord_active.lib.common.metric import AnnotationType, DataType, Metric, MetricType
from encord_active.lib.common.writer import CSVMetricWriter

logger = logger.opt(colors=True)


class AnnotationTimeMetric(Metric):
    TITLE = "Annotation Time"
    SHORT_DESCRIPTION = "Ranks annotations by the time it took to make them."
    LONG_DESCRIPTION = r"""Ranks annotations by the time it took to make them.

If no logs are available for a particular object, it will get score 0."""
    METRIC_TYPE = MetricType.HEURISTIC
    DATA_TYPE = DataType.IMAGE
    ANNOTATION_TYPE = AnnotationType.ALL
    SCORE_NORMALIZATION = True

    def test(self, iterator: Iterator, writer: CSVMetricWriter):
        found_any = False

        for data_unit, img_pth in iterator.iterate(desc="Computing annotation times"):
            for object in data_unit["labels"]["objects"]:
                object_label_logs = iterator.get_label_logs(object_hash=object["objectHash"])

                if not object_label_logs:
                    writer.write_score(objects=object, score=0.0, description="No logs available.")
                    continue

                times = map(lambda x: x.get("time_taken", None) or 0.0, object_label_logs)
                writer.write_score(object, score=sum(times) / 1000, description="Annotation time (seconds).")
                found_any = True

        if not found_any:
            logger.info("<blue>[Note]</blue> Couldn't get any label logs. All objects will have score 0.")
