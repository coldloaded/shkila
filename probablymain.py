def main():

    def gui():
        import io
        from os.path import join
        import PySimpleGUIQt as sg
        from PIL import Image as PImage
        import easyocr as ocr
        from re import fullmatch, compile

        sg.theme("DefaultNoMoreNagging")

        file_types = [("JPEG (*.jpg)", "*.jpg"),
                      ("PNG (*.png)","*.png"),
                      ("All files (*.*)", "*.*")]

        file_list_column = [[sg.Text("Load images to model"),
                             sg.In(enable_events=True,key='file_added',visible=False),
                             sg.FilesBrowse(file_types=file_types)],
                            [sg.Listbox(values=set(),enable_events=True,key="file_list")],
                            [sg.Button("Convert to plain text!",key="convert",disabled=True,button_color=("white","gray"))]]

        image_preview = [[sg.Text("Image preview:",size_px=(320,20))],
                         [sg.Image(key="image_view",size_px=(320, 320))]]

        text_preview = [[sg.Text("Text preview:")],
                        [sg.Listbox(values=[],key="text_view")],
                        [sg.FileSaveAs("save this one",enable_events=True, key="save_individual")],
                        [sg.FolderBrowse("save all",enable_events=True,key="save_all")]]

        layout = [[sg.Column(file_list_column),
                   sg.Column(image_preview),
                   sg.Column(text_preview,key="text_column",visible=False)]]

        window = sg.Window(title="Image-to-text converter",layout=layout)
        converted_text = dict()
        reader = ocr.Reader(["ru","en"])
        state = False
        last = ''
        pattern = compile(r".*/([^/]+)")

        while True:
            event,values = window.read()

            if event == "file_added":
                window["file_list"].update(values = window["file_list"].Values | set(values["file_added"].split(';')))

            elif event == "file_list" and values["file_list"]:
                filename = values["file_list"][0]
                if filename!=last:
                    last = filename
                    image = PImage.open(values["file_list"][0])
                    image.thumbnail((320, 320))
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
                    window["image_view"].update(data=bio.getvalue())
                if state:
                    try: window["text_view"].update(values = [converted_text[last]])
                    except: window["text_view"].update(values = [''])
                else:
                    window["convert"].update(disabled=False,button_color=("white","blue"))

            elif event == "convert":
                for img in window["file_list"].Values:
                    if img in converted_text.keys(): continue
                    else: converted_text[img] = '\n'.join(reader.readtext(img,detail=0))
                window["text_column"].update(visible=True)
                window["text_view"].update(values = [converted_text[last]])
                state = True

            elif event == "save_individual":
                with io.open(f"{values['save_individual'][0]}.txt",'w',encoding="UTF-8") as file:
                    file.write(converted_text[last])
                    file.close()

            elif event == "save_all":
                pth = values["save_all"]
                for filename in converted_text.keys():
                    with open(join(pth,f"{fullmatch(pattern,filename).group(1)}.txt"),'w',encoding="UTF-8") as file:
                        file.write(converted_text[filename])
                        file.close()

            elif event == sg.WINDOW_CLOSED:
                window.close()
                break

    gui()

if __name__ == "__main__":
    main()