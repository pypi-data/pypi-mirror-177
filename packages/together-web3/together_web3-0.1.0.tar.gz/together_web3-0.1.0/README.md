# @togethercomputer/together-web3.py [![build](https://github.com/togethercomputer/together-web3.py/actions/workflows/build.yml/badge.svg)](https://github.com/togethercomputer/together-web3.py/actions/workflows/build.yml)

```python
from together_web3.computer import LanguageModelInferenceRequest
from together_web3.together import TogetherWeb3

together_web3 = TogetherWeb3()
result = await together_web3.language_model_inference(
    from_dict(
        data_class=LanguageModelInferenceRequest,
        data={
            "model": "gpt2",
            "prompt": "George Washington was the first",
        }
    ),
)
print("result", result)
```

See [examples/example.py](examples/example.py)

### Generate an image

```console
python examples/example.py "Rainbow unicorn" "StableDiffusion" \
  | grep image_base64 | cut -d\" -f4 | base64 -d > x.jpg && open x.jpg
```

