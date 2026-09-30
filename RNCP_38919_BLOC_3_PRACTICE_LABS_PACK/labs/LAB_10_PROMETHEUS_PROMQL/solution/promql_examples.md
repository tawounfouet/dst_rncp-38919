# PromQL patterns

```promql
<real_metric_name>
```

```promql
sum(rate(<real_counter_metric>[5m]))
```

```promql
sum by (<real_label>) (rate(<real_counter_metric>[5m]))
```
