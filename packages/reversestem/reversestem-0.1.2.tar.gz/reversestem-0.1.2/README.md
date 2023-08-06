# Reverse Stemming (reversestem)
Stemming is the technique or method of reducing words with similar meaning into their “stem” or “root” form.

Reverse stemming takes a “stem” or “root” form and returns all the words that have this root as a basis.

## Usage
```python
from reversestem import unstem

unstem('aggreg')
```

outputs the stems grouped by lemma
```json
{
   "aggregability":[],
   "aggregable":[],
   "aggregant":[
      "aggregants"
   ],
   "aggregate":[
      "aggregated",
      "aggregately",
      "aggregateness"
   ],
   "aggregating":[],
   "aggregation":[
      "aggregational"
   ],
   "aggregative":[
      "aggregatives",
      "aggregatively",
      "aggregativeness"
   ],
   "aggregativity":[],
   "aggregator":[]
}
```

Or a flat list can be produced like this
```python
unstem('aggreg', flatten=True)
```

and this outputs a simple list
```json
[
   "aggregativeness",
   "aggregational",
   "aggregability",
   "aggregateness",
   "aggregativity",
   "aggregatively",
   "aggregatives",
   "aggregating",
   "aggregation",
   "aggregately",
   "aggregative",
   "aggregated",
   "aggregable",
   "aggregants",
   "aggregator",
   "aggregate",
   "aggregant"
]
```
