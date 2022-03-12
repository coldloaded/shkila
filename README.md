# shkila

To install this application, simpy initialise a new python project with virtual enviroment, and then follow this simple instruction:

If you are able to use this application on a CUDA-featured device, run this command in the main project folder via terminal:
  pip3 install torch torchvision torchaudio easyocr Pillow
  
Otherwise run this two commands:
  pip3 install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
  pip3 install Pillow easyocr
