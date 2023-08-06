# Fast Sentence Classification (fast-sentence-classify)

## Sample Usage
```python
from fast_sentence_classify import classify

d_result = classify("I'd like it if you could give me some directions to the library")
```
Result:
```json
{
   "data":{
      "input_text":"I'd like it if you could give me some directions to the library",
      "output_text":"WHERE_LOCATION"
   },
   "event":"fast-sentence-classify",
   "service":"classify",
   "stopwatch":"117.30μs",
   "ts":"1666897985.085184"
}
```
