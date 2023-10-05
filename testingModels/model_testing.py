'''
CS3250 - Software Development Methods and Tools - Fall 2023
Project 01- Windoors
Description: This program is meant for testing the data model
Group Name: Backroom Gang
Developed by: Joseph Tewolde
'''
# These are the imports for the program
from sqlalchemy import * 
from sqlalchemy.engine import *
from sqlalchemy.orm import *

# This is the base class for the program
class Base(DeclarativeBase):
    pass

# This is the user class for the program
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True) # user id
    email = Column(String, unique=True, nullable=False) # email address
    passwd = Column(String) # password 
    creationDate = Column(String) # date of creation

# This is the ResellerUser class for the program
class Reseller(User):
    __tablename__ = "reseller"
    id = Column(String, ForeignKey("users.id"), primary_key=True) # user id
    company = Column(String()) # company name
    address = Column(String()) # company address
    phone = Column(String()) # company phone number
    website = Column(String()) # company website
    orders = relationship("Order", cascade="delete") # reselluser orders

# This is the AdminUser class for the program
class Admin(User):
    __tablename__ = "admin"
    id = Column(String, ForeignKey("users.id"), primary_key=True) # user id
    name = Column(String()) # admin name
    title = Column(String()) # admin title

# This is the Product class for the program
class Product(Base):
    __tablename__ = "products"
    code = Column(String, primary_key=True) # product code
    description = Column(String) # product description
    type = Column(String) # product type
    available = Column(Boolean) # product availability
    price = Column(Float) # product price

# This is the Order class for the program
class Order(Base):
    __tablename__ = "orders" 

    number = Column(String(), primary_key=True) # order number
    creation_date = Column(String()) # order creation date
    status = Column(String()) # order status

    # Establish a one-to-many relationship between Order and Items
    items = relationship("Item", cascade="delete") # order items

    # Establish a many-to-one relationship between Order and Users
    reseller_id = Column(String, ForeignKey("reseller.id"), primary_key = True) # user id

# This is the Item class for the program
class Item(Base):
    __tablename__ = "items"

    orderNumber = Column(String(), ForeignKey("orders.number"), primary_key=True) # order number
    sequetialNumber = Column(Integer()) # item sequential number
    productCode = Column(String(), ForeignKey("products.code")) # product code
    quantity = Column(Integer()) # item quantity
    specs = Column(String()) # item specifications

    # Establish a one-to-many relationship between Order and Items
    order = relationship("Order", back_populates="items") # order items
    # Establish a one-to-one relationship between Item and Product
    product = relationship("Product") # item product

if __name__ == "__main__": 

    engine = create_engine('sqlite:///app.db')
    Base.metadata.create_all(engine) # creates all tables from your model classes
    Session = sessionmaker(engine)
    session = Session()
    with session:

        # create a User
        user = User(id = 'jtewolde', email = 'JMurray@gmail.com', passwd = '123', creationDate = '2021-09-01')

        # create a Reseller user
        reseller = Reseller(id = 'tmota', email= 'backroomgang@gmail.com', passwd= '3829', creationDate= '2021-12-21', company='Backroom Gang', address='1234 Main St', phone='123-456-7890', website='www.backroomgang.com')
        reseller2 = Reseller(id = 'Bsolz', email = 'LKIAB@yahoo.com', passwd = '123', creationDate = '2021-09-02', company = 'LKIAB', address = '1234 Main St', phone = '123-456-7890', website = 'www.LKIAB.com')


        # create an Admin user
        admin = Admin(id = 'Bryan', email = 'jtewold@aol.com', passwd = 'denver', creationDate = '2021-09-03',name='Joseph Tewolde', title='Developer')

        # create a Product
        product = Product(code='PRD001', description='Product 001', type='Window', available=True, price=100.00)
        product2 = Product(code='PRD002', description='Product 002', type='Door', available=True, price=200.00)

        # create an Order
        # order = Order(number='ORD001', creation_date='2021-09-01', status='Pending')
        # order2 = Order(number='ORD002', creation_date='2021-09-02', status='Delivered')

        # create an Item
        item = Item(orderNumber= 'ORD001', sequetialNumber=1, productCode='PRD001', quantity=1, specs='Specs')
        item2 = Item(orderNumber= 'ORD002', sequetialNumber=2, productCode='PRD002', quantity=2, specs='Specs')
        item3 = Item(orderNumber= 'ORD003', sequetialNumber=3, productCode='PRD003', quantity=3, specs='Specs')
        item4 = Item(orderNumber= 'ORD004', sequetialNumber=4, productCode='PRD004', quantity=4, specs='Specs')

        order = Order(number='ORD001', creation_date='2021-09-01', status='Pending', reseller_id = reseller.id)
        order2 = Order(number='ORD002', creation_date='2021-09-02', status='Delivered', reseller_id = reseller.id)

        order3 = Order(number='ORD002', creation_date='2021-09-03', status='Pending', reseller_id = reseller2.id)
        order4 = Order(number='ORD004', creation_date='2021-09-04', status='Delivered', reseller_id = reseller2.id)

        # add the User to the session
        session.add(user)
        # add the Reseller user to the session
        session.add(reseller)
        session.add(reseller2)
        # add the Admin user to the session
        session.add(admin)
        # add the Product to the session
        session.add(product)
        session.add(product2)
        # add the Order to the session
        session.add(order)
        session.add(order2)
        session.add(order3)
        session.add(order4)
        # add the Item to the session
        session.add(item)
        session.add(item2)
        session.add(item3)
        session.add(item4)

        # commit the session
        session.commit()

        # Query all users
        all_users = session.query(User).all()
        for user in all_users:
            print(f"User ID: {user.id}, Email: {user.email}, Password: {user.passwd}, Creation Date: {user.creationDate}")

        print("\n")

        # Query all resellers
        all_resellers = session.query(Reseller).all()
        for reseller in all_resellers:
            print(f"User ID: {reseller.id}, Email: {reseller.email}, Password: {reseller.passwd}, Creation Date: {reseller.creationDate}, Company: {reseller.company}, Address: {reseller.address}, Phone: {reseller.phone}, Website: {reseller.website}")
        
        print("\n")

        # Query all admins
        all_admins = session.query(Admin).all()
        for admin in all_admins:
            print(f"User ID: {admin.id}, Email: {admin.email}, Password: {admin.passwd}, Creation Date: {admin.creationDate}, Name: {admin.name}, Title: {admin.title}")

        print("\n")

        # Query all products
        all_products = session.query(Product).all()
        for product in all_products:
            print(f"Code: {product.code}, Description: {product.description}, Type: {product.type}, Available: {product.available}, Price: {product.price}")

        print("\n")

        # Query all orders
        all_orders = session.query(Order).all()
        for order in all_orders:
            print(f"Number: {order.number}, Creation Date: {order.creation_date}, Status: {order.status}")

        print("\n")

        # Query all items
        all_items = session.query(Item).all()
        for item in all_items:
            print(f"Order Number: {item.orderNumber}, Sequential Number: {item.sequetialNumber}, Product Code: {item.productCode}, Quantity: {item.quantity}, Specs: {item.specs}")

        print("\n")

    ######################################################### TESTING RELATIONSHIPS #########################################################
        # Query all items with their order
        all_items = session.query(Item).join(Order).all()
        for item in all_items:
            print(f"Order Number: {item.orderNumber}, Sequential Number: {item.sequetialNumber}, Product Code: {item.productCode}, Quantity: {item.quantity}, Specs: {item.specs}, Order Number: {item.order.number}, Creation Date: {item.order.creation_date}, Status: {item.order.status}")

        print("\n")

        # Query all orders for a reseller user
        all_orders = session.query(Order).join(Reseller).all()
        for order in all_orders:
            Treseller = session.query(Reseller).filter(Reseller.id == order.reseller_id).first()
            print(
                f"Number: {order.number}, Creation Date: {order.creation_date}, "
                f"Status: {order.status}, Reseller ID: {order.reseller_id}, "
                f"User ID: {Treseller.id}, Email: {Treseller.email}, "
                f"Password: {Treseller.passwd}, Creation Date: {Treseller.creationDate}"
            )
        print("\n")

        # Test the 

        
