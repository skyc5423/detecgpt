from segment_anything_hq import SamPredictor, sam_model_registry, SamAutomaticMaskGenerator
import numpy as np


class SamInferencer:
    def __init__(self):
        sam = sam_model_registry["vit_l"](checkpoint="./sam_vit_l_0b3195.pth")
        self.predictor = SamPredictor(sam)

    def predict_sam(self, image_pil, bbox_prompt):
        img = np.array(image_pil)
        self.predictor.set_image(img)
        masks = self.predictor.predict(box=bbox_prompt)[0]
        mask = masks[0]
        return mask
