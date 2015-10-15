DROP VIEW IF EXISTS public.road_view;
DROP VIEW IF EXISTS public.town_view;
DROP TABLE IF EXISTS public.school;
DROP SEQUENCE IF EXISTS public.school_id_seq;
DROP TABLE IF EXISTS public.road;
DROP SEQUENCE IF EXISTS public.road_id_seq;
DROP TABLE IF EXISTS public.road_info;
DROP SEQUENCE IF EXISTS public.road_info_id_seq;
DROP TABLE IF EXISTS public.town;
DROP TABLE IF EXISTS public.city;

CREATE TABLE public.city
(
  id varchar(1),
  geom geometry(MultiPolygon, 3826),
  city_name varchar(6),
  english_name varchar(30),

  CONSTRAINT CITYPK 
    PRIMARY KEY (id)
);

CREATE TABLE public.town
(
  id varchar(3),
  geom geometry(MultiPolygon, 3826),
  town_name varchar(8),
  english_name varchar(30),
  zipcode varchar(3),
  city_no varchar(1),

  CONSTRAINT TOWNPK 
    PRIMARY KEY (id),   
  CONSTRAINT TOWNFK_CITY 
    FOREIGN KEY (city_no) REFERENCES city(id)
);

CREATE SEQUENCE public.school_id_seq START 1; 
CREATE TABLE public.school
(
  id integer NOT NULL DEFAULT nextval('school_id_seq'::regclass),
  geom geometry(Point, 3826),
  school_name varchar(90),
  code varchar(90),

  CONSTRAINT SCHOOLPK 
    PRIMARY KEY (id)
);

CREATE SEQUENCE public.road_info_id_seq START 1; 
CREATE TABLE public.road_info
(
  id integer NOT NULL DEFAULT nextval('road_info_id_seq'::regclass),
  road_name varchar(100),
  full_name varchar(100),
  type varchar(30),
  kind varchar(8),
  
  CONSTRAINT ROADINFOPK 
    PRIMARY KEY (id)
);

CREATE SEQUENCE public.road_id_seq START 1; 
CREATE TABLE public.road
(
  id integer NOT NULL DEFAULT nextval('road_id_seq'::regclass),
  geom geometry(MultiLineString, 3826),
  info_no integer,
  town_no varchar(3),

  CONSTRAINT ROADPK 
    PRIMARY KEY (id),   
  CONSTRAINT ROADFK_TOWN 
    FOREIGN KEY (town_no) REFERENCES town(id),
  CONSTRAINT ROADFK_ROADINFO	
    FOREIGN KEY (info_no) REFERENCES road_info(id)
);

CREATE VIEW public.road_view AS
SELECT T2.id, T2.geom, T2.road_name, T2.full_name, T2.type, T2.kind, T2.town_name, C.city_name
FROM public.city C JOIN (SELECT T1.id, T1.geom, T1.road_name, T1.full_name, T1.type, T1.kind, TOW.town_name, TOW.city_no
			 FROM public.town TOW JOIN (SELECT L.id, L.geom, L.town_no, R.road_name, R.full_name, R.type, R.kind
					            FROM public.road L JOIN public.road_info R ON L.info_no = R.id
                                                    ORDER BY L.id) T1 ON TOW.id = T1.town_no) T2 ON C.id = T2.city_no;

CREATE VIEW public.town_view AS
SELECT T.id, T.geom, T.town_name, T.english_name, T.zipcode, C.city_name
FROM public.town T JOIN public.city C ON T.city_no = C.id; 
