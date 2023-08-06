from looqbox.json_encoder import JsonEncoder
from abc import ABC, abstractmethod
import json


class BaseRender(ABC):

    remove_nones = True

    @staticmethod
    def _dict_to_json(object_as_dict: dict) -> json:
        """"
        Convert a dict to Looqbox's json structure
        """
        json_content = json.dumps(object_as_dict, indent=1, allow_nan=True, cls=JsonEncoder)
        return json_content

    def remove_json_nones(self, json_dict: dict) -> dict:
        # Used in tests to check if the json structure is correct
        if not self.remove_nones:
            return json_dict

        # Get all the keys from empty (None) dict values
        if isinstance(json_dict, (dict, list)):
            empty_key_vals = [key for key, value in json_dict.items() if not value and not isinstance(value, bool)]
            # Delete the empty keys
            for key in empty_key_vals:
                del json_dict[key]

            json_dict = self.remove_nones_from_children_fields(json_dict)
        return json_dict

    def remove_nones_from_children_fields(self, json_dict):
        for key in json_dict.keys():
            if isinstance(json_dict[key], list):
                json_dict[key] = [self.remove_json_nones(json_component) for json_component in json_dict[key]]
            elif isinstance(json_dict[key], dict):
                json_dict[key] = self.remove_json_nones(json_dict[key])
        return json_dict

    @abstractmethod
    def response_board_render(self, board, remove_nones=True):
        """
        Method used to convert local objects to Looqbox's front-end syntax
        """

    @abstractmethod
    def response_frame_render(self, frame, remove_nones=True):
        pass

    @abstractmethod
    def file_upload_render(self, obj_file_upload, remove_nones=True):
        pass

    @abstractmethod
    def html_render(self, obj_html, remove_nones=True):
        pass

    @abstractmethod
    def pdf_render(self, obj_pdf, remove_nones=True):
        pass

    @abstractmethod
    def simple_render(self, obj_simple, remove_nones=True):
        pass

    @abstractmethod
    def image_render(self, obj_image, remove_nones=True):
        pass

    @abstractmethod
    def list_render(self, obj_list, remove_nones=True):
        pass

    @abstractmethod
    def message_render(self, obj_message, remove_nones=True):
        pass

    @abstractmethod
    def query_render(self, obj_query, remove_nones=True):
        pass

    @abstractmethod
    def table_render(self, obj_table, remove_nones=True):
        pass

    @abstractmethod
    def web_frame(self, obj_web, remove_nones=True):
        pass

    @abstractmethod
    def text_render(self, obj_text, remove_nones=True):
        pass

    @abstractmethod
    def plotly_render(self, obj_plotly, remove_nones=True):
        pass

    @abstractmethod
    def audio_render(self, obj_audio, remove_nones=True):
        pass

    @abstractmethod
    def video_render(self, obj_video, remove_nones=True):
        pass

    @abstractmethod
    def switch_render(self, obj_switch, remove_nones=True):
        pass

    @abstractmethod
    def tooltip_render(self, obj_tooltip, remove_nones=True):
        pass

    @abstractmethod
    def link_render(self, obj_tooltip, remove_nones=True):
        pass

    @abstractmethod
    def row_render(self, obj_row, remove_nones=True):
        pass

    @abstractmethod
    def column_render(self, obj_column, remove_nones=True):
        pass

    @abstractmethod
    def gauge_render(self, obj_gauge, remove_nones=True):
        pass

    @abstractmethod
    def line_render(self, obj_shape, remove_nones=True):
        pass

    @abstractmethod
    def embed_render(self, obj_embed, remove_nones=True):
        pass

    @abstractmethod
    def obj_form_render(self, obj_form, remove_nones=True):
        pass

    @abstractmethod
    def form_html_render(self, obj_form_html, remove_nones=True):
        pass

    @abstractmethod
    def image_capture_render(self, obj_image_capture, remove_nones=True):
        pass
