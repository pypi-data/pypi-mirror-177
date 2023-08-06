# entity-classification

Perform Entity Classification via two inputs: `entity_names: list` and `input_tokens: list`

Assume you wish to classify `network_topology` and you have these tokens extracted from your text:
```python
[
    'edge', 
    'network',
    'moderate', 
    'cat5', 
    'topology', 
    'locate'
]
```

Use this code
```python
from entity_classification import classify

classify(entity_names=['network_topology'], input_tokens=input_tokens)
```

The result will be
```python
{
    'result': ['network_topology'],
    'tokens': ['network', 'topology']
}
```