DROP TABLE IF EXISTS product_details.products;
DROP TABLE IF EXISTS product_details.watch_list;
DROP TABLE IF EXISTS product_details.watch_attr_dict;

CREATE TABLE product_details.products(
	id BIGINT NOT NULL
	, name TEXT NOT NULL
	, allegro_url TEXT NOT NULL
	, price NUMERIC(10,2) NOT NULL
	, sku BIGINT NOT NULL
	, availability TEXT NOT NULL
	, offer_attributes JSONB
	, product_attributes JSONB
	, category_path TEXT NOT NULL
	, category VARCHAR(200) NOT NULL
	, category_hash INT
	, CONSTRAINT cn_001 PRIMARY KEY(id)
);
CREATE INDEX cat_md5_indx ON product_details.products(category_hash);


CREATE TABLE product_details.watch_attr_dict(
	watch_attr_id SERIAL4 NOT NULL
	, watch_attr_name VARCHAR(100) NOT NULL
	, attr_storage VARCHAR(100) NOT NULL
	, CONSTRAINT cn_wad_001_pk PRIMARY KEY(watch_attr_id)
);


CREATE TABLE product_details.watch_list(
	product_id BIGINT NOT NULL
	, watch_attr_id INT NOT NULL
	, watch_id SERIAL4 NOT NULL
	, last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	, watch_action VARCHAR(50) DEFAULT 'NO ACTION'
	, CONSTRAINT cn_wl_001_pk PRIMARY KEY(product_id, watch_attr_id)
	, CONSTRAINT cn_wl_002_fk FOREIGN KEY(product_id) REFERENCES product_details.products(id) ON DELETE CASCADE
	, CONSTRAINT cn_wl_003_fk FOREIGN KEY(watch_attr_id) REFERENCES product_details.watch_attr_dict(watch_attr_id) ON DELETE CASCADE
);