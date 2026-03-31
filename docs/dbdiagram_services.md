# Organizing your schema into **independent services (microservices or modular monolith domains)** 

## 1. Identity Service

Handles authentication, user accounts, and profiles.

Responsibilities:

* user login/register
* profile management
* user avatar
* address book

Tables:

```dbml
Table users {
  id uuid [pk]
  email varchar [unique, not null]
  password_hash varchar
  role varchar
  created_at timestamptz
}

Table user_profiles {
  user_id uuid [pk]
  full_name varchar
  phone varchar
  avatar_media_id uuid
}

Table addresses {
  id uuid [pk]
  user_id uuid
  street varchar
  city varchar
  state varchar
  country varchar
  postal_code varchar
  created_at timestamptz
}

Ref: user_profiles.user_id > users.id
Ref: user_profiles.avatar_media_id > media.id
Ref: addresses.user_id > users.id
```

---

## 2. Media Service

Centralized file storage for images/videos.

Used by:

* avatars
* brand logos
* product images
* review images

Tables:

```dbml
Table media {
  id uuid [pk]
  url varchar
  media_type varchar
  mime_type varchar
  size int
  created_at timestamptz
}
```

---

## 3. Catalog Service

Responsible for **product discovery**.

Responsibilities:

* products
* categories
* brands
* variants
* attributes
* product images

Tables:

```dbml
Table categories {
  id uuid [pk]
  name varchar
  parent_id uuid
}

Table brands {
  id uuid [pk]
  name varchar [not null, unique]
  slug varchar [unique]
  description text
  website varchar
  logo_media_id uuid
  created_at timestamptz
  updated_at timestamptz
}

Table products {
  id uuid [pk]
  title varchar
  description text
  brand_id uuid
  slug varchar
  created_at timestamptz
  published_at timestamptz
  status varchar
}

Table product_categories {
  product_id uuid
  category_id uuid

  indexes {
    (product_id, category_id) [pk]
  }
}

Table product_variants {
  id uuid [pk]
  product_id uuid
  sku varchar [unique]
  price numeric
  compare_at_price numeric
  created_at timestamptz
}

Table variant_media {
  id uuid [pk]
  variant_id uuid
  media_id uuid
  position int
  is_primary boolean
}

Table attributes {
  id uuid [pk]
  name varchar
}

Table attribute_values {
  id uuid [pk]
  attribute_id uuid
  value varchar
}

Table variant_attributes {
  variant_id uuid
  attribute_value_id uuid
}

Ref: categories.parent_id > categories.id
Ref: brands.logo_media_id > media.id
Ref: products.brand_id > brands.id
Ref: product_categories.product_id > products.id
Ref: product_categories.category_id > categories.id
Ref: product_variants.product_id > products.id
Ref: variant_media.variant_id > product_variants.id
Ref: variant_media.media_id > media.id
Ref: attribute_values.attribute_id > attributes.id
Ref: variant_attributes.variant_id > product_variants.id
Ref: variant_attributes.attribute_value_id > attribute_values.id
```

---

## 4. Inventory Service

Handles stock and warehouses.

Responsibilities:

* stock levels
* reservations
* warehouse locations

Tables:

```dbml
Table warehouses {
  id uuid [pk]
  name varchar
  location varchar
}

Table inventory_items {
  id uuid [pk]
  variant_id uuid
  warehouse_id uuid
  quantity int
  reserved int
}

Ref: inventory_items.variant_id > product_variants.id
Ref: inventory_items.warehouse_id > warehouses.id
```

---

## 5. Cart Service

Handles temporary user shopping carts.

Responsibilities:

* add/remove items
* cart calculation

Tables:

```dbml
Table carts {
  id uuid [pk]
  user_id uuid
  created_at timestamptz
}

Table cart_items {
  id uuid [pk]
  cart_id uuid
  product_id uuid
  variant_id uuid
  quantity int
}

Ref: carts.user_id > users.id
Ref: cart_items.cart_id > carts.id
Ref: cart_items.product_id > products.id
Ref: cart_items.variant_id > product_variants.id
```

---

## 6. Order Service

Responsible for **checkout and order lifecycle**.

Responsibilities:

* create order
* calculate totals
* store order items
* snapshot shipping/billing addresses

Tables:

```dbml
Table orders {
  id uuid [pk]
  user_id uuid
  status varchar
  payment_status varchar
  fulfillment_status varchar
  subtotal_amount numeric
  discount_amount numeric
  tax_amount numeric
  shipping_amount numeric
  total_amount numeric
  currency varchar
  created_at timestamptz
  updated_at timestamptz
}

Table order_items {
  id uuid [pk]
  order_id uuid
  product_id uuid
  variant_id uuid
  quantity int
}

Table order_addresses {
  id uuid [pk]
  order_id uuid
  type varchar
  full_name varchar
  phone varchar
  street varchar
  city varchar
  state varchar
  country varchar
  postal_code varchar
}

Ref: orders.user_id > users.id
Ref: order_items.order_id > orders.id
Ref: order_items.product_id > products.id
Ref: order_items.variant_id > product_variants.id
Ref: order_addresses.order_id > orders.id
```

---

## 7. Payment Service

Handles financial transactions.

Responsibilities:

* payment processing
* transaction tracking
* refunds

Tables:

```dbml
Table payments {
  id uuid [pk]
  order_id uuid
  provider varchar
  amount numeric
  status varchar
  created_at timestamptz
}

Ref: payments.order_id > orders.id
```

---

## 8. Fulfillment / Shipping Service

Responsible for order delivery.

Responsibilities:

* shipments
* tracking numbers
* shipping status

Tables:

```dbml
Table shipments {
  id uuid [pk]
  order_id uuid
  carrier varchar
  tracking_number varchar
  status varchar
}

Ref: shipments.order_id > orders.id
```

---

## 9. Review / Social Service

Handles product feedback and interactions.

Responsibilities:

* reviews
* review media
* comments
* reactions

Tables:

```dbml
Table product_reviews {
  id uuid [pk]
  product_id uuid [not null]
  user_id uuid [not null]
  rating int
  title varchar
  content text
  verified_purchase boolean
  likes_count int [default: 0]
  comments_count int [default: 0]
  created_at timestamptz
  updated_at timestamptz
}

Table review_media {
  review_id uuid
  media_id uuid

  indexes {
    (review_id, media_id) [pk]
  }
}

Table review_comments {
  id uuid [pk]
  review_id uuid [not null]
  user_id uuid [not null]
  parent_id uuid
  content text
  created_at timestamptz
}

Table reactions {
  id uuid [pk]
  user_id uuid
  entity_type varchar
  entity_id uuid
  reaction_type varchar
  created_at timestamptz

  indexes {
    (user_id, entity_type, entity_id) [unique]
  }
}

Ref: product_reviews.product_id > products.id
Ref: product_reviews.user_id > users.id
Ref: review_media.review_id > product_reviews.id
Ref: review_media.media_id > media.id
Ref: review_comments.review_id > product_reviews.id
Ref: review_comments.user_id > users.id
Ref: review_comments.parent_id > review_comments.id
Ref: reactions.user_id > users.id
```

---

## Final Architecture Overview

Your platform naturally splits into **9 services**:

```
Identity Service
Media Service
Catalog Service
Inventory Service
Cart Service
Order Service
Payment Service
Fulfillment Service
Review Service
```

High-level dependency flow:

```
Users → Cart → Order
            ↓
        Inventory
            ↓
        Payment
            ↓
        Shipment
```

Product discovery flow:

```
Catalog → Media
        → Reviews
```
