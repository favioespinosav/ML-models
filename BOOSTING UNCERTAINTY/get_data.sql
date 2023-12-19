with step1 as(
select  product_name,toStartOfWeek(dt, 1) AS monday, max(price) as max_price,count(*) as y from default.data_sales_train 
group by product_name,toStartOfWeek(dt, 1)),

step2 as(

select *, lagInFrame(y, 1) OVER (PARTITION BY product_name ORDER BY monday) AS y_lag_1,
lagInFrame(y, 2) OVER (PARTITION BY product_name ORDER BY monday) AS y_lag_2,
lagInFrame(y, 3) OVER (PARTITION BY product_name ORDER BY monday) AS y_lag_3,
lagInFrame(y, 4) OVER (PARTITION BY product_name ORDER BY monday) AS y_lag_4,
lagInFrame(y, 5) OVER (PARTITION BY product_name ORDER BY monday) AS y_lag_5 ,
lagInFrame(y, 6) OVER (PARTITION BY product_name ORDER BY monday) AS y_lag_6,

sum(y) OVER (PARTITION BY product_name ORDER BY monday ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS y_avg_3,
max(y) OVER (PARTITION BY product_name ORDER BY monday ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS y_max_3,
count(y) OVER (PARTITION BY product_name ORDER BY monday ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS y_count_3,
count(y) OVER (PARTITION BY product_name ORDER BY monday ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING) AS y_count_6,
min(y) OVER (PARTITION BY product_name ORDER BY monday ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS y_min_3,


sum(y) OVER (PARTITION BY product_name ORDER BY monday ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING) AS y_avg_6,
max(y) OVER (PARTITION BY product_name ORDER BY monday ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING) AS y_max_6,
min(y) OVER (PARTITION BY product_name ORDER BY monday ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING) AS y_min_6

from step1),

step3 as(

select monday,sum(y_lag_1) y_all_lag_1,sum(y_lag_2) y_all_lag_2,sum(y_lag_3) y_all_lag_3,
sum(y_lag_4) y_all_lag_4,sum(y_lag_5) y_all_lag_5,sum(y_lag_6) y_all_lag_6, 
sum(y_avg_3)/3 y_all_avg_3, min(y_min_3) y_all_min_3,
sum(y_avg_6)/6 y_all_avg_6,max(y_max_6) y_all_max_6, min(y_min_6) y_all_min_6 from step2 group by monday )


select o.product_name,o.monday,o.max_price,o.y,y_lag_1,o.y_lag_2,o.y_lag_3,o.y_lag_4,o.y_lag_5,o.y_lag_6, o.y_avg_3/3 as y_avg_3, 
o.y_max_3, if(o.y_count_3 <3, 0, o.y_min_3) as y_min_3, 
o.y_avg_6/6 as y_avg_6,
o.y_max_6, if(o.y_count_6 <6, 0, o.y_min_6) as y_min_6,
r.y_all_lag_1,r.y_all_lag_2,r.y_all_lag_3,r.y_all_lag_4,r.y_all_lag_5,r.y_all_lag_6



,r.y_all_avg_3,GREATEST(r.y_all_lag_1,r.y_all_lag_2,r.y_all_lag_3) as y_all_max_3,LEAST(r.y_all_lag_1,r.y_all_lag_2,r.y_all_lag_3) as y_all_min_3,r.y_all_avg_6,
GREATEST(r.y_all_lag_1,r.y_all_lag_2,r.y_all_lag_3,r.y_all_lag_4,r.y_all_lag_5,r.y_all_lag_6) as y_all_max_6,
LEAST(r.y_all_lag_1,r.y_all_lag_2,r.y_all_lag_3,r.y_all_lag_4,r.y_all_lag_5,r.y_all_lag_6)  y_all_min_6

  
from step2 o  left join step3  r  using(monday)  order by product_name,monday














