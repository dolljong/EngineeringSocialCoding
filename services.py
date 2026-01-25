from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os
import yaml
from src.utils import create_sample_dxf, display_dxf
from src.models import CustomTableModel

class DxfService:
    @staticmethod
    def load_dxf(parent, selected_item):
        if selected_item:
            if selected_item[0] == "부모 항목 2":
                parent.display_image("resources/pic01.jpg")
            else:
                doc = create_sample_dxf(selected_item[0], selected_item[1])
                display_dxf(doc, parent.view.scene())
        else:
            QMessageBox.warning(parent, "선택 오류", "트리 메뉴에서 항목을 선택해주세요.")

    @staticmethod
    def save_dxf(parent, selected_item):
        if selected_item:
            doc = create_sample_dxf(selected_item[0], selected_item[1])
            display_dxf(doc, parent.view.scene())
            filename = f"{selected_item[0]}_{selected_item[1]}.dxf"
            doc.saveas(filename)
            QMessageBox.information(parent, "저장 완료", f"{filename} 파일이 저장되었습니다.")
        else:
            QMessageBox.warning(parent, "선택 오류", "트리 메뉴에서 항목을 선택해주세요.")