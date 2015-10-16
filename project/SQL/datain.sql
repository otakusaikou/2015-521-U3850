 -- Insert city data

INSERT INTO public.city
SELECT code,
       geom,
       cityname,
       ecityname
FROM public.cityin;


DROP TABLE IF EXISTS public.cityin;

 -- Insert town data

INSERT INTO public.town
SELECT TOW.code,
       TOW.geom,
       TOW.townname,
       TOW.etownname,
       TOW.zipcode,
       C.id
FROM public.townin TOW,
     public.city C
WHERE ST_Intersects(TOW.geom, C.geom);


DROP TABLE IF EXISTS public.townin;

 -- Replace NULL values with string 'NONE' in the input source table 'roadin'.

UPDATE public.roadin
SET txt = 'NONE'
WHERE txt IS NULL;


UPDATE public.roadin
SET fullname = 'NONE'
WHERE fullname IS NULL;

 -- Insert road data

INSERT INTO public.road_info
SELECT nextval('road_info_id_seq'::regclass),
       T.*
FROM
  (SELECT DISTINCT txt,
                   fullname,
                   TYPE,
                   kind
   FROM public.roadin
   ORDER BY txt) T;


INSERT INTO public.road
SELECT nextval('road_id_seq'::regclass),
       geom,
       L.id,
       town
FROM public.road_info L,
     public.roadin R
WHERE L.road_name = R.txt
  AND L.full_name = R.fullname
  AND L.TYPE = R.TYPE
  AND L.kind = R.kind;


DROP TABLE IF EXISTS public.roadin;

 -- Replace NULL values with string 'NONE' in the input source table 'schoolin'.

UPDATE public.schoolin
SET code = 'NONE'
WHERE code IS NULL;

 -- Insert school data

INSERT INTO public.school
SELECT nextval('school_id_seq'::regclass),
       SC.geom,
       SC.txtname,
       SC.code
FROM public.schoolin SC;


DROP TABLE IF EXISTS public.schoolin;
