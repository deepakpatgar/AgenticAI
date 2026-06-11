from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from flask import Flask, render_template, request


app = Flask(__name__)


@dataclass(frozen=True)
class RoomType:
    slug: str
    name: str
    nightly_rate: int
    description: str
    perks: list[str]


@dataclass(frozen=True)
class MenuItem:
    slug: str
    name: str
    category: str
    price: int
    description: str


@dataclass(frozen=True)
class ServiceItem:
    slug: str
    name: str
    price: int
    description: str


ROOM_TYPES = [
    RoomType(
        slug="suite",
        name="Skyline Suite",
        nightly_rate=240,
        description="A panoramic suite with lounge seating and a private dining nook.",
        perks=["City view", "Butler service", "Complimentary minibar"],
    ),
    RoomType(
        slug="deluxe",
        name="Deluxe King Room",
        nightly_rate=170,
        description="A bright, modern room with a deep soaking tub and work desk.",
        perks=["King bed", "Rain shower", "Late checkout"],
    ),
    RoomType(
        slug="family",
        name="Family Studio",
        nightly_rate=210,
        description="Two-zone layout with extra seating and room for a rollaway bed.",
        perks=["Extra beds", "Breakfast included", "Kid-friendly menu"],
    ),
]

MENU_ITEMS = [
    MenuItem(
        slug="truffle-pasta",
        name="Truffle Cream Pasta",
        category="Chef Specials",
        price=28,
        description="Silky pasta with parmesan, herbs, and a light truffle finish.",
    ),
    MenuItem(
        slug="royal-thali",
        name="Royal Thali Platter",
        category="Signature Dining",
        price=32,
        description="A generous platter of curries, breads, rice, and chutneys.",
    ),
    MenuItem(
        slug="garden-salad",
        name="Garden Harvest Salad",
        category="Light Bites",
        price=16,
        description="Crisp greens, citrus dressing, seeds, and avocado.",
    ),
    MenuItem(
        slug="dessert-tower",
        name="Dessert Tower",
        category="Sweet Finish",
        price=22,
        description="Mini mousse cups, fruit tartlets, and a warm chocolate bite.",
    ),
]

EXTRA_SERVICES = [
    ServiceItem(
        slug="airport-pickup",
        name="Airport Pickup",
        price=40,
        description="Luxury airport transfer with bottled water and luggage help.",
    ),
    ServiceItem(
        slug="spa-access",
        name="Spa Access",
        price=55,
        description="Full access to sauna, steam room, and relaxation lounge.",
    ),
    ServiceItem(
        slug="late-checkout",
        name="Late Checkout",
        price=30,
        description="Stay until 2 PM with guaranteed room retention.",
    ),
]


def parse_int(value: str | None, default: int) -> int:
    try:
        parsed = int(value or "")
        return max(parsed, 0)
    except ValueError:
        return default


def parse_date(value: str | None, default: date) -> date:
    if not value:
        return default
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return default


class WelcomeAgent:
    def build_highlights(self) -> list[str]:
        return [
            "24-hour concierge and curated city guides",
            "Panoramic rooftop lounge and indoor pool",
            "Chef-led dining with room service till midnight",
        ]


class RoomAgent:
    def recommend(self, room: RoomType, nights: int, guests: int) -> str:
        if room.slug == "suite" or guests > 2:
            return f"{room.name} is ideal for {guests} guests over {nights} nights."
        return f"{room.name} balances comfort and value for your {nights}-night stay."


class DiningAgent:
    def summarize(self, ordered_items: list[dict[str, object]]) -> str:
        if not ordered_items:
            return "No dining items selected yet. Pick dishes to build your bill."
        featured = ordered_items[0]["name"]
        return f"Your dining cart is anchored by {featured}, with chef specials and desserts ready to add."


class BillingAgent:
    tax_rate = 0.12
    service_rate = 0.08

    def calculate(
        self,
        room: RoomType,
        nights: int,
        menu_items: list[dict[str, object]],
        services: list[dict[str, object]],
    ) -> dict[str, object]:
        room_total = room.nightly_rate * nights
        menu_total = sum(item["total"] for item in menu_items)
        service_total = sum(item["price"] for item in services)
        subtotal = room_total + menu_total + service_total
        tax = round(subtotal * self.tax_rate, 2)
        service_charge = round(subtotal * self.service_rate, 2)
        total = round(subtotal + tax + service_charge, 2)

        return {
            "room_total": room_total,
            "menu_total": menu_total,
            "service_total": service_total,
            "subtotal": subtotal,
            "tax": tax,
            "service_charge": service_charge,
            "total": total,
        }


def build_selected_room(room_slug: str | None) -> RoomType:
    return next((room for room in ROOM_TYPES if room.slug == room_slug), ROOM_TYPES[0])


def build_menu_cart(form_data: dict[str, str]) -> list[dict[str, object]]:
    cart: list[dict[str, object]] = []
    for item in MENU_ITEMS:
        quantity = parse_int(form_data.get(f"qty_{item.slug}"), 0)
        if quantity <= 0:
            continue
        cart.append(
            {
                "slug": item.slug,
                "name": item.name,
                "category": item.category,
                "price": item.price,
                "quantity": quantity,
                "total": item.price * quantity,
                "description": item.description,
            }
        )
    return cart


def build_menu_quantities(form_data: dict[str, str]) -> dict[str, int]:
    quantities: dict[str, int] = {}
    for item in MENU_ITEMS:
        quantities[item.slug] = parse_int(form_data.get(f"qty_{item.slug}"), 0)
    return quantities


def build_selected_services(form_data: dict[str, str]) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    for service in EXTRA_SERVICES:
        if form_data.get(service.slug):
            selected.append(
                {
                    "slug": service.slug,
                    "name": service.name,
                    "price": service.price,
                    "description": service.description,
                }
            )
    return selected


def run_hotel_agents(form_data: dict[str, str]) -> dict[str, object]:
    today = date.today()
    guest_name = (form_data.get("guest_name") or "Avery Guest").strip() or "Avery Guest"
    adults = parse_int(form_data.get("adults"), 2) or 1
    nights = parse_int(form_data.get("nights"), 2) or 1
    check_in = parse_date(form_data.get("check_in"), today)
    room = build_selected_room(form_data.get("room_type"))

    menu_cart = build_menu_cart(form_data)
    menu_quantities = build_menu_quantities(form_data)
    services = build_selected_services(form_data)
    selected_service_slugs = {service["slug"] for service in services}

    welcome_agent = WelcomeAgent()
    room_agent = RoomAgent()
    dining_agent = DiningAgent()
    billing_agent = BillingAgent()

    quote = billing_agent.calculate(room, nights, menu_cart, services)
    check_out = check_in + timedelta(days=nights)
    room_note = room_agent.recommend(room, nights, adults)
    dining_note = dining_agent.summarize(menu_cart)

    return {
        "guest_name": guest_name,
        "adults": adults,
        "nights": nights,
        "check_in": check_in,
        "check_out": check_out,
        "room": room,
        "menu_cart": menu_cart,
        "services": services,
        "quote": quote,
        "highlights": welcome_agent.build_highlights(),
        "room_note": room_note,
        "dining_note": dining_note,
        "menu_items": MENU_ITEMS,
        "room_types": ROOM_TYPES,
        "extra_services": EXTRA_SERVICES,
        "menu_quantities": menu_quantities,
        "selected_service_slugs": selected_service_slugs,
    }


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    form_data = request.form.to_dict(flat=True) if request.method == "POST" else {
        "guest_name": "Avery Guest",
        "adults": "2",
        "nights": "2",
        "room_type": "suite",
        "check_in": date.today().isoformat(),
        "qty_truffle-pasta": "1",
        "qty_royal-thali": "1",
        "airport-pickup": "on",
    }

    context = run_hotel_agents(form_data)
    context["is_post"] = request.method == "POST"
    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
