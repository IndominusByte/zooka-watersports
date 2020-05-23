import json, io, os
from basetest import BaseTest
from services.models.UserModel import User
from services.models.CategoryModel import Category
from services.models.ActivityModel import Activity

class VoucherTest(BaseTest):
    def test_00_add_2_user(self):
        self.register(self.EMAIL_TEST)
        self.register(self.EMAIL_TEST_2)

        self.assertTrue(User.query.filter_by(email=self.EMAIL_TEST).first())
        self.assertTrue(User.query.filter_by(email=self.EMAIL_TEST_2).first())

    def test_01_create_category(self):
        user = User.query.filter_by(email=self.EMAIL_TEST).first()
        user.role = 2
        user.save_to_db()
        # login user 1
        self.login(self.EMAIL_TEST)

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())

        with self.app() as client:
            res = client.post('/category/create',content_type=self.content_type,data={'image': (img,'image.jpg'),'name': self.NAME},
                headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"})
            self.assertEqual(201,res.status_code)
            self.assertEqual("Success add category.",json.loads(res.data)['message'])

    def test_02_create_activity(self):
        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())
        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img2 = io.BytesIO(im.read())
        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img3 = io.BytesIO(im.read())
        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img4 = io.BytesIO(im.read())

        category = Category.query.filter_by(name=self.NAME).first()
        # success add activity
        with self.app() as client:
            res = client.post('/activity/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                data={'image':(img, 'image.jpg'),'image2': (img2, 'image.jpg'),'image3': (img3, 'image.jpg'),'image4': (img4, 'image.jpg'),
                    'name': self.NAME,'description':'asds','duration':'dwqwdq',
                    'category_id':category.id,'discount':20,'price':10000,'min_person':2,
                    'include':'dwqdwq','pickup':'dwqdwq','information':'dwqdwq'})
            self.assertEqual(201,res.status_code)
            self.assertEqual("Success add activity.",json.loads(res.data)['message'])

    def test_03_validation_create_voucher(self):
        # check image required
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                data={'image':''})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Missing data for required field."],json.loads(res.data)['image'])
        # check dangerous file
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                data={'image': (io.BytesIO(b"print('sa')"), 'test.py')})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Cannot identify image file"],json.loads(res.data)['image'])

        with open(os.path.join(self.DIR_IMAGE,'test.gif'),'rb') as im:
            img = io.BytesIO(im.read())
        # check file extension
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image': (img,'test.gif')})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Image must be jpg|png|jpeg"],json.loads(res.data)['image'])

        with open(os.path.join(self.DIR_IMAGE,'size.png'),'rb') as im:
            img = io.BytesIO(im.read())
        # file can't be grater than 4 Mb
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                data={'image': (img,'size.png')})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Image cannot grater than 4 Mb"],json.loads(res.data)['image'])

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())
        # check title,code,valid_start,valid_end,description,discount,type_voucher,minimum,terms blank
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'title':'','code':'','valid_start':'',
                        'valid_end':'','description':'','discount':'','type_voucher':'',
                        'minimum':'','terms':''})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Length must be between 5 and 100."],json.loads(res.data)['title'])
            self.assertListEqual(["Length must be between 5 and 100."],json.loads(res.data)['code'])
            self.assertListEqual(["Length must be between 3 and 100."],json.loads(res.data)['valid_start'])
            self.assertListEqual(["Length must be between 3 and 100."],json.loads(res.data)['valid_end'])
            self.assertListEqual(["Shorter than minimum length 5."],json.loads(res.data)['description'])
            self.assertListEqual(["Not a valid integer."],json.loads(res.data)['discount'])
            self.assertListEqual(["Length must be between 3 and 100."],json.loads(res.data)['type_voucher'])
            self.assertListEqual(["Not a valid integer."],json.loads(res.data)['minimum'])
            self.assertListEqual(["Shorter than minimum length 5."],json.loads(res.data)['terms'])

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())
        # check discount,minimum,activity_id minus number
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'type_voucher':'Person','discount':-1,'minimum':-1,'activity_id':-1})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Value must be greater than 0"],json.loads(res.data)['discount'])
            self.assertListEqual(["Value must be greater than 0"],json.loads(res.data)['minimum'])
            self.assertListEqual(["Value must be greater than 0"],json.loads(res.data)['activity_id'])

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())
        # invalid date format for valid_start & valid_end
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'valid_start':'dwqdwqdwq','valid_end':'dqwdwqw'})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Invalid date format."],json.loads(res.data)['valid_start'])
            self.assertListEqual(["Invalid date format."],json.loads(res.data)['valid_end'])

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())

        # discount cannot less than IDR 10k
        # type voucher mustbe Transaction or Person
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'type_voucher':'dwqwdqd','discount':12})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Discount cannot less than IDR. 10.000"],json.loads(res.data)['discount'])
            self.assertListEqual(["Invalid voucher type."],json.loads(res.data)['type_voucher'])

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())

        # activity not found
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'activity_id':99999})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Activity not found"],json.loads(res.data)['activity_id'])

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())
        # if type voucher Person cannot grater than 100 person
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'title':'dqwdqd','code':'dwqdwqd',
                        'valid_start':'2019-10-31','valid_end':'2019-10-31','description':'dqwdwq',
                        'discount':10000,'terms':'dwqdqq','type_voucher':'Person','minimum':1000})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Minimum cannot greater than 100"],json.loads(res.data)['minimum'])

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())
        # if type voucher Transaction cannot less than IDR 10k
        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'title':'dqwdqd','code':'dwqdwqd',
                        'valid_start':'2019-10-31','valid_end':'2019-10-31','description':'dqwdwq',
                        'discount':10000,'terms':'dwqdwq','type_voucher':'Transaction','minimum':1})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["Minimum cannot less than IDR. 10.000"],json.loads(res.data)['minimum'])

    def test_04_create_voucher(self):
        activity = Activity.query.filter_by(name=self.NAME).first()

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())

        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'title':self.NAME,'code':self.NAME,'valid_start':'2019-10-31',
                        'valid_end':'2019-10-31','description':'dwqdwqdqw','discount':10000,'type_voucher':'Person',
                        'minimum':2,'terms':'dqwdwqdwq','activity_id':activity.id})
            self.assertEqual(201,res.status_code)
            self.assertEqual('Success add voucher.',json.loads(res.data)['message'])

    def test_05_title_code_already_taken(self):
        # title , code already taken
        activity = Activity.query.filter_by(name=self.NAME).first()

        with open(os.path.join(self.DIR_IMAGE,'image.jpg'),'rb') as im:
            img = io.BytesIO(im.read())

        with self.app() as client:
            res = client.post('/voucher/create',content_type=self.content_type,headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"},
                    data={'image':(img,'image.jpg'),'title':self.NAME,'code':self.NAME,'valid_start':'2019-10-31',
                        'valid_end':'2019-10-31','description':'dwqdwqdqw','discount':10000,'type_voucher':'Person',
                        'minimum':2,'terms':'dqwdwqdwq','activity_id':activity.id})
            self.assertEqual(400,res.status_code)
            self.assertListEqual(["The title has already been taken."],json.loads(res.data)['title'])
            self.assertListEqual(["The code has already been taken."],json.loads(res.data)['code'])

    def test_97_delete_activity(self):
        activity = Activity.query.filter_by(name=self.NAME).first()
        with self.app() as client:
            res = client.delete('/activity/crud/{}'.format(activity.id),headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"})
            self.assertEqual(200,res.status_code)
            self.assertEqual("Success delete activity.",json.loads(res.data)['message'])

    def test_98_delete_category(self):
        category = Category.query.filter_by(name=self.NAME).first()
        with self.app() as client:
            res = client.delete('/category/crud/{}'.format(category.id),headers={'Authorization':f"Bearer {self.ACCESS_TOKEN}"})
            self.assertEqual(200,res.status_code)
            self.assertEqual("Success delete category.",json.loads(res.data)['message'])

    def test_99_delete_user_from_db(self):
        user = User.query.filter_by(email=self.EMAIL_TEST).first()
        user.delete_from_db()
        user = User.query.filter_by(email=self.EMAIL_TEST_2).first()
        user.delete_from_db()
