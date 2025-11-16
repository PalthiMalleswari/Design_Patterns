
from typing import Optional,Dict,List
from enum import Enum
import datetime

class VehicleType(Enum):
    CAR = "Car"
    TRUCK = "Truck"
    ELECTRIC_CAR = "ElectriCar"
    MOTARBIKE = "Motarbike"

class ParkingSpotType(Enum):

    DISABLED = "Disabled"
    COMPACT = "Compact"
    LARGE = "Large"
    MOTORCYCLE = "Motorcycle"
    ELECTRIC_CAR = "ElectricCar"
    MOTORBIKE = "Motorbike"


class Vehicle:
    def __init__(self,reg_no:str,type:VehicleType):
        self.reg_no = reg_no
        self.type = type
    def get_vehicle_type(self):
        return self.type
    def get_vehicle_regis_num(self):
        return self.reg_no
    
class ParkingSpot:

    def __init__(self,parking_spot_id:str,spot_type:ParkingSpotType,vehicle:Optional[Vehicle]=None):
        self.is_free = True
        self.parking_spot_id = parking_spot_id
        self.spot_type = spot_type
        self.vehicle = vehicle

    def assign_vehicle_to_spot(self,vehicle:Vehicle):
        self.vehicle = vehicle
        self.is_free = False
    def vacate_vehicle_from_spot(self):
        self.vehicle = None
        self.is_free = True
        
    def is_spot_free(self):
        return self.is_free
    
class ParkingFloor:
    def __init__(self,floor_id:str):
        self.floor_id = floor_id
        self.parking_spots : Dict[ParkingSpotType,List[ParkingSpot]] = {}

    def get_list_of_parking_spots(self):
        return self.parking_spots
    
class ParkingTicket:
    def __init__(self,parking_ticket_id:str,vehicle:Vehicle,parking_spot_id:str,parking_floor_id:str):
        self.parking_ticket_id = parking_ticket_id
        self.vehicle = vehicle
        self.parking_spot_id = parking_spot_id
        self.parking_floor_id = parking_floor_id
        self.start_time = datetime.now()
        self.end_time:Optional[datetime] = None
        self.amount: Optional[float] = None

    
class HourlyCost:
    def __init__(self):
        self.hourly_costs: Dict[ParkingSpotType,float] = {}

    def get_cost(self,parking_spot_type:ParkingSpotType):
        return self.hourly_costs.get(parking_spot_type,0.0)
        
class Payment:
    def __init__(self,hourly_cost:HourlyCost):
        self.hourly_cost = hourly_cost

    def calculate_parking_fee(self,parking_spot_type:ParkingSpotType,duration:int):
        return self.hourly_cost.get_cost(parking_spot_type)*duration


class EntryPanel:
    def __init__(self,entry_panel_id:str):
        self.entry_panel_id = entry_panel_id

    def generate_parking_ticket(self,vehicle:Vehicle,parking_floor_id:str,parking_spot_id:str):
        ticket_id = f"T-{vehicle.reg_no}-{datetime.now().timestamp()}"
        return ParkingTicket(ticket_id,vehicle,parking_spot_id,parking_floor_id)
        

class ExitPannel:
    def __init__(self,exit_pannel_id:str):
        self.exit_pannel_id = exit_pannel_id

    def checkout_parking_fee(self,parking_ticket:ParkingTicket,payment:Payment):
        duration = (datetime.now() - parking_ticket.start_time).seconds//3600
        fee = payment.calculate_parking_fee(parking_ticket.vehicle.get_vehicle_type(),duration)
        parking_ticket.amount = fee
        parking_ticket.end_time = datetime.now()
        return fee

class ParkingLot:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ParkingLot,cls).__new__(cls)
        return cls._instance
    def __init__(self):
        self.parking_floors:List[ParkingFloor] = []
        self.entry_pannels: List[EntryPanel] = []
        self.exit_pannels:List[ExitPannel] = []

    def get_instance(self):
        return self._instance
    

parking = ParkingLot()
print(parking)
print(parking.parking_floors)




