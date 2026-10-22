from decimal import Decimal
from django.core.management.base import BaseCommand
from catalog.models import Product, SizeOption, PaperOption, PrintOption, FinishingOption, QuantityPrice

PRODUCTS = {
'Business Cards': {'category':'print','sizes':[('3.5 × 2 in',0),('3.75 × 2.25 in',30)],'papers':[('300 GSM',300,1),('350 GSM',350,1.12),('400 GSM',400,1.25)],'printing':[('Full Color — Single Side',0),('Full Color — Both Sides',0.35)],'finish':[('Matte Lamination',250,0.15),('Gloss Lamination',220,0.12),('Soft Touch',400,0.22),('Cutting',0,0.03)],'prices':[(100,2499,12.0),(250,999,9.0),(1000,None,7.0)]},
'Flyers': {'category':'print','sizes':[('A5',0),('A4',40),('A3',90)],'papers':[('80 GSM',80,0.8),('100 GSM',100,1),('130 GSM Art Paper',130,1.25)],'printing':[('Full Color — Single Side',0),('Full Color — Both Sides',0.75)],'finish':[('Folding',300,0.05),('Cutting',0,0.02)],'prices':[(100,499,8.0),(500,999,5.5),(1000,None,4.0)]},
'Brochures': {'category':'print','sizes':[('A4 Tri-fold',0),('A3 Bi-fold',80)],'papers':[('130 GSM Art Paper',130,1),('170 GSM Art Paper',170,1.18)],'printing':[('Full Color — Both Sides',0)],'finish':[('Folding',350,0.08),('Matte Lamination',500,0.2)],'prices':[(100,499,18.0),(500,999,13.0),(1000,None,9.5)]},
'Posters': {'category':'print','sizes':[('A3',0),('A2',120),('A1',280)],'papers':[('130 GSM Art Paper',130,1),('200 GSM',200,1.3)],'printing':[('Full Color — Single Side',0)],'finish':[('Cutting',0,0.05)],'prices':[(10,49,180.0),(50,99,140.0),(100,None,110.0)]},
'Stickers': {'category':'custom','sizes':[('3 × 3 in',0),('4 × 4 in',40)],'papers':[('Sticker Paper',0,1),('Vinyl',0,1.45)],'printing':[('Full Color — Single Side',0)],'finish':[('Cutting',0,0.25)],'prices':[(50,199,20.0),(200,499,15.0),(500,None,10.0)]},
'Photo Printing': {'category':'photo','sizes':[('4 × 6 in',0),('5 × 7 in',25),('8 × 10 in',60)],'papers':[('Photo Paper',0,1),('Premium Photo Paper',0,1.35)],'printing':[('Full Color — Single Side',0)],'finish':[],'prices':[(1,49,80.0),(50,199,55.0),(200,None,45.0)]},
'Wall Wallpaper': {'category':'large','sizes':[('Custom — per sq ft',0),('Custom — per sq m',0)],'papers':[('Wallpaper Media',0,1),('Premium Textured Wallpaper',0,1.3)],'printing':[('Full Color — Single Side',0)],'finish':[('Trim / Cut',0,0.15)],'prices':[(20,99,65.0),(100,499,55.0),(500,None,45.0)]},
'Large Format Vinyl': {'category':'large','sizes':[('Custom — per sq ft',0)],'papers':[('Self-Adhesive Vinyl',0,1),('Premium Vinyl',0,1.25)],'printing':[('Full Color — Single Side',0)],'finish':[('Trim / Cut',0,0.12)],'prices':[(10,49,80.0),(50,199,65.0),(200,None,55.0)]},
}
class Command(BaseCommand):
    help='Create editable demo products and pricing rules for RANL PRINT.'
    def handle(self,*args,**kwargs):
        for name,cfg in PRODUCTS.items():
            p,_=Product.objects.update_or_create(name=name, defaults={'category':cfg['category'],'active':True})
            p.sizes.all().delete(); p.papers.all().delete(); p.printing_options.all().delete(); p.finishing_options.all().delete(); p.quantity_prices.all().delete()
            for label,delta in cfg['sizes']: SizeOption.objects.create(product=p,name=label,price_delta=Decimal(str(delta)))
            for label,gsm,mult in cfg['papers']: PaperOption.objects.create(product=p,name=label,gsm=gsm or None,multiplier=Decimal(str(mult)))
            for label,delta in cfg['printing']: PrintOption.objects.create(product=p,name=label,price_delta=Decimal(str(delta)))
            for label,fixed,unit in cfg['finish']: FinishingOption.objects.create(product=p,name=label,fixed_fee=Decimal(str(fixed)),per_unit_fee=Decimal(str(unit)))
            for minq,maxq,unit in cfg['prices']: QuantityPrice.objects.create(product=p,min_quantity=minq,max_quantity=maxq,unit_price=Decimal(str(unit)))
            self.stdout.write(self.style.SUCCESS(f'Seeded {p.name}'))
