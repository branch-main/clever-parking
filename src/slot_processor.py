class SlotProcessor:
    def __init__(self):
        self.last_known_slots = ["?", "?", "?"]

    def extract_data(self, result):
        print(f"Extracting data from result type: {type(result)}")
        
        if isinstance(result, list) and len(result) > 0:
            first_result = result[0]
            print(f"Result keys: {first_result.keys()}")
            predictions_data = first_result.get("predictions", {})
            predictions_list = predictions_data.get("predictions", [])
            label_visualization = first_result.get("label_visualization")
            print(f"Has label_visualization: {label_visualization is not None}")
            if label_visualization:
                print(f"Label visualization type: {type(label_visualization)}")
                # Si es un dict, extraer el valor base64
                if isinstance(label_visualization, dict):
                    label_visualization = label_visualization.get("value")
                    print(f"Extracted value from dict, length: {len(label_visualization) if label_visualization else 0}")
                else:
                    print(f"Label visualization length: {len(label_visualization)} chars")
            return predictions_list, label_visualization
        elif "outputs" in result and len(result["outputs"]) > 0:
            output = result["outputs"][0]
            print(f"Output keys: {output.keys()}")
            predictions_list = output.get("predictions", {}).get("predictions", [])
            label_visualization = output.get("label_visualization")
            print(f"Has label_visualization: {label_visualization is not None}")
            if label_visualization:
                print(f"Label visualization type: {type(label_visualization)}")
                # Si es un dict, extraer el valor base64
                if isinstance(label_visualization, dict):
                    label_visualization = label_visualization.get("value")
                    print(f"Extracted value from dict, length: {len(label_visualization) if label_visualization else 0}")
                else:
                    print(f"Label visualization length: {len(label_visualization)} chars")
            return predictions_list, label_visualization
        return [], None

    def process_predictions(self, predictions_list):
        print(f"Found {len(predictions_list)} predictions")

        for pred in predictions_list:
            x = pred.get("x", 0)
            class_id = pred.get("class_id", 0)
            class_name = pred.get("class", "unknown")
            confidence = pred.get("confidence", 0)
            print(
                f"Prediction: x={x}, class_id={class_id}, class={class_name}, conf={confidence:.2f}"
            )

        predictions_list.sort(key=lambda p: p.get("x", 0))

        slots = ["?", "?", "?"]
        for idx, pred in enumerate(predictions_list):
            if idx < 3:
                class_id = pred.get("class_id", 0)
                slots[idx] = "O" if class_id == 0 else "L"
                print(f"Slot {idx} = {slots[idx]} (x={pred.get('x', 0)})")

        for i in range(3):
            if slots[i] != "?":
                self.last_known_slots[i] = slots[i]
            else:
                slots[i] = self.last_known_slots[i]

        print(f"Final slots: {slots}")
        return slots
