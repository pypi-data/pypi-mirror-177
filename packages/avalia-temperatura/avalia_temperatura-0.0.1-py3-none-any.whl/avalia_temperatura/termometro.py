def temperatura(celsius):
   if celsius <= 35:
      print('hipotermia')
   elif celsius >= 35.1 and celsius <= 37.7:
         print('temperatura corporal normal')
   elif celsius >=37.8 and  celsius <=38.5:
         print('febre leve')
   elif celsius >=38.6 and celsius <=39.4:
         print('febre moderada')
   elif celsius >= 39.5:
         print('febre grave')
   return""