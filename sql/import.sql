\copy customers   from 'C:/Users/darin/desktop/nomad-market/data/customers.csv'   with (format csv, header true);
\copy suppliers   from 'C:/Users/darin/desktop/nomad-market/data/suppliers.csv'   with (format csv, header true);
\copy products    from 'C:/Users/darin/desktop/nomad-market/data/products.csv'    with (format csv, header true);
\copy orders      from 'C:/Users/darin/desktop/nomad-market/data/orders.csv'      with (format csv, header true);
\copy order_items from 'C:/Users/darin/desktop/nomad-market/data/order_items.csv' with (format csv, header true);
\copy payment     from 'C:/Users/darin/desktop/nomad-market/data/payment.csv'     with (format csv, header true);
\copy shipments   from 'C:/Users/darin/desktop/nomad-market/data/shipments.csv'   with (format csv, header true);
\copy reviews     from 'C:/Users/darin/desktop/nomad-market/data/reviews.csv'     with (format csv, header true);
