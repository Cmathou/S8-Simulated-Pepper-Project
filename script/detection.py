import Algorithmia

class detection:
    def detect(self,path):

        client = Algorithmia.client('simhBkZ0DJroYl2ZNAJsJKEfZWU1')

        imfile = "data://Benjaminlegrosbg/images/detection.png"

        # Upload local file
        client.file(imfile).putFile(path)

        input = {
          "image": imfile,
          "output": "data://.algo/deeplearning/ObjectDetectionCOCO/temp/detection.png",
          "min_score": 0.5,
          "model": "ssd_mobilenet_v1"
        }

        algo = client.algo('deeplearning/ObjectDetectionCOCO/0.2.1')
        algo.set_options(timeout=300) # optional
        
        if len(algo.pipe(input).result[u'boxes']) > 3:
	        type_obj = []
	        coord = []
	        for obj in algo.pipe(input).result[u'boxes']:
		        type_obj.append(obj[u'label'])
		        coord.append(obj[u'coordinates'])
	        return [type_obj,coord]
        else:
	        type_obj = []
	        coord = []
	        for obj in algo.pipe(input).result[u'boxes']:
		        type_obj.append(obj[u'label'])
		        coord.append(obj[u'coordinates'])
	        return [type_obj,coord]
