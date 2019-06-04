import Algorithmia

client = Algorithmia.client('simhBkZ0DJroYl2ZNAJsJKEfZWU1')

imfile = "data://Benjaminlegrosbg/images/test.png"

#if client.file(imfile).exists() is False:
    # Upload local file
client.file(imfile).putFile("../images/test.png")

input = {
  "image": imfile,
  "output": "data://.algo/deeplearning/ObjectDetectionCOCO/temp/test.png",
  "min_score": 0.7,
  "model": "ssd_mobilenet_v1"
}

algo = client.algo('deeplearning/ObjectDetectionCOCO/0.2.1')
algo.set_options(timeout=300) # optional


if len(algo.pipe(input).result[u'boxes']) == 3:
	type_obj = []
	coord = []
	for obj in algo.pipe(input).result[u'boxes']:
		type_obj.append(obj[u'label'])
		coord.append(obj[u'coordinates'])
	print(type_obj)
	print(coord)	
else:
	print(algo.pipe(input).result)
		


