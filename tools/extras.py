# manual items: (box, src, EN, SV, opts)
def L(box,src,en,sv,**o): return dict(box=box,src=src,EN=en,SV=sv,**o)
EXTRA={
 '49':[L([30,338,196,353],'Настройки успешно импортированы','Settings imported successfully','Inställningarna importerades',center=True,tighten=True)],
 '56':[L([11,88,220,102],'Выбрано: W, Up','Selected: W, Up','Valda: W, Up',tighten=True)],
 '65':[L([14,152,56,164],'Робот','Robot','Robot',tighten=True)],
 '10':[L([40,157,184,168],'Сервер RoboCam выключен','RoboCam server is off','RoboCam-servern är avstängd',center=True,tighten=True)],
 '12':[ # robocam-06 diagram, centred labels
  L([159,36,278,49],'Средним мотором','The medium motor','Medelmotorn',fg=[34,34,34],center=True,maxw=150),
  L([162,57,275,67],'наклоняем рамку','tilts the frame','lutar ramen',fg=[34,34,34],center=True,maxw=150),
  L([359,19,534,32],'Преобразуем координату z','We convert the z coordinate','Vi omvandlar z-koordinaten',fg=[34,34,34],center=True,maxw=205),
  L([355,37,536,50],'джойстика B в команды для','of joystick B into commands for','för styrspak B till kommandon för',fg=[34,34,34],center=True,maxw=205),
  L([347,58,545,68],'управления средним мотором','controlling the medium motor','styrning av medelmotorn',fg=[34,34,34],center=True,maxw=205),
  L([578,36,761,49],'Передаём координату точки','We send the coordinate of the','Vi skickar koordinaten för',fg=[34,34,34],center=True,maxw=185),
  L([578,54,761,67],'прикосновения к джойстику','touch point on the joystick','beröringspunkten på styrspaken',fg=[34,34,34],center=True,maxw=185),
  L([576,390,762,402],'Передаём координаты точки','We send the coordinates of the','Vi skickar koordinaterna för',fg=[34,34,34],center=True,maxw=185),
  L([578,407,761,421],'прикосновения к джойстику','touch point on the joystick','beröringspunkten på styrspaken',fg=[34,34,34],center=True,maxw=185),
  L([339,388,539,401],'Преобразуем координаты x и y','We convert the x and y coordinates','Vi omvandlar x- och y-koordinaterna',fg=[34,34,34],center=True,maxw=210),
  L([347,404,529,421],'джойстика A в команды для','of joystick A into commands for','för styrspak A till kommandon för',fg=[34,34,34],center=True,maxw=210),
  L([330,424,546,438],'управления большими моторами','controlling the large motors','styrning av de stora motorerna',fg=[34,34,34],center=True,maxw=210),
  L([160,405,296,418],'Большими моторами','The large motors','De stora motorerna',fg=[34,34,34],center=True,maxw=140),
  L([182,424,273,436],'крутим колёса','turn the wheels','vrider hjulen',fg=[34,34,34],center=True,maxw=140),
 ],
 '31':[
  L([173,10,266,24],'Точка касания','Touch point','Beröringspunkt',fg=[20,20,20]),
  L([146,32,307,48],'Вычисленная координата','Calculated coordinate','Beräknad koordinat',maxw=168,fg=[20,20,20]),
 ],
 '40':[ # export toast: file name lines
  L([26,201,197,212],'RoboCam_Исследователь_EV3_2','RoboCam_EV3_Explorer_2016','RoboCam_EV3_Explorer_2016'),
  L([26,214,99,223],'016-10-18.xml','-10-18.xml','-10-18.xml'),
 ],
 '48':[ # file-picker: file names (wrapped as in the original)
  L([41,172,218,184],'RoboCam_Гоночная_машин','RoboCam_Racing_car_spe','RoboCam_Racerbil_snabb'),
  L([41,189,208,201],'а_скоростн._2016-10-06.x','ed_2016-10-06.xml','_2016-10-06.xml'),
  L([41,204,54,214],'ml','',''),
  L([41,227,213,239],'RoboCam_Исследователь_','RoboCam_EV3_Explorer_','RoboCam_EV3_Explorer_'),
  L([41,243,191,255],'EV3_11_2016-09-29.xml','11_2016-09-29.xml','11_2016-09-29.xml'),
  L([41,265,214,278],'RoboCam_Робот_с_клешнё','RoboCam_Claw_robot_201','RoboCam_Klorobot_2016-'),
  L([41,281,153,294],'й_2016-10-16.xml','6-10-16.xml','10-16.xml'),
 ],
}
