# UrbanLivabilityScore

## Installing the package:

```python
pip install urbanlivabilityscore
```

## Syntax

```python
street_lighting_score(road_width, number_of_poles)
# road_width and number_of_poles are expected to be arrays
```

## Few ways of using the package

```python
from urbanlivabilityscore import street_lighting_score
street_lighting_score(road_width, number_of_poles)
```

```python
from urbanlivabilityscore import street_lighting_score as sls
sls(road_width, number_of_poles)
```

```python
import urbanlivabilityscore
urbanlivabilityscore.street_lighting_score(road_width, number_of_poles)
```

```python
import urbanlivabilityscore as uls
uls.street_lighting_score(road_width, number_of_poles)
```
