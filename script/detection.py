imfile = "data://Benjaminlegrosbg/images/avion.jpg"

if client.file(imfile).exists() is False:
    # Upload local file
    client.file(imfile).putFile("avion.jpg")

input = {
  "image": imfile,
  "output": "data://.algo/deeplearning/ObjectDetectionCOCO/temp/suit_and_tie.png",
  "min_score": 0.7,
  "model": "ssd_mobilenet_v1"
}

algo = client.algo('deeplearning/ObjectDetectionCOCO/0.2.1')
algo.set_options(timeout=300) # optional
print(algo.pipe(input).result)
