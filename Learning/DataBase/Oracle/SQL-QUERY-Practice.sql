CREATE TABLE Employee (
    employee_id int,
    last_name varchar(255),
    first_name varchar(255),
    salary number(18,2),
    create_date date default sysdate
);


select * from food_sales for update;


-- Nth highest total price
select * from food_sales s1
where 5 = (select count( distinct s2.totalprice) 
          from food_sales s2 
          where s2.totalprice > s1.totalprice
          )

-- Top N highest totalprice 
select distinct s.totalprice 
from food_sales s
order by s.totalprice desc 
FETCH FIRST 5 ROWS ONLY;

-- Find duplicate rows in the table based on totalprice
select * from food_sales where totalprice in (select totalprice 
from food_sales 
group by totalprice
having count(totalprice) > 1
)
order by totalprice desc

-- select / delete duplicate rows from table

with T as (
select product, totalprice
       ,row_number() over (partition by product, totalprice order by product, totalprice) as row_num
from food_sales        
)
select * from  T where T.row_num > 1;



with T as (
select product, totalprice
       ,row_number() over (partition by product, totalprice order by product, totalprice) as row_num
from food_sales        
)
select * from food_sales s, T where s.totalprice= T.totalprice and s.product = T.product and T.row_num > 1;


-- analytic functions
select e.*,
       row_number() over (partition by e.sal  order by e.sal desc ) as top_rec
       , rank() over (order by e.sal desc) as rank_sal
       , rank() over (partition by e.deptno order by e.sal) as rank_dep_sal
       , dense_rank() over (partition by e.deptno order by e.sal) as dense_rank_sal
       , count(*) over (partition by e.deptno) as dep_emp_count
       , min(e.sal) over (partition by e.deptno) as dep_min_sal
       , sum (e.sal) over () as total_sal
       , sum(e.sal) over (partition by e.deptno) as dep_total_sal
       , first_value (e.sal) over (partition by e.deptno order by e.sal desc) as dep_first_sal
       , last_value(e.sal) over (partition by e.deptno order by e.sal desc ROWS BETWEEN
           UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING ) as dep_last_sal
from EMP e
order by e.deptno

-- Nth highest salary
select e1.*
from EMP e1
where 2= (select count(distinct e2.sal) from EMP e2 where e2.sal > e1.sal) 