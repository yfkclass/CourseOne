select * from Frequency where docid = '10398_txt_earn'

select term from Frequency where docid = '10398_txt_earn' and count = 1

select term from Frequency where docid = '10398_txt_earn' and count = 1
union
select term from Frequency where docid = '925_txt_trade' and count = 1

select count(*) from (select distinct docid from Frequency where term = 'legal' or term = 'law') x;

select docid, count(Frequency.term)  from Frequency
group by docid
having count(Frequency.term) > 300


select * from (select docid from Frequency where term = 'transactions') x
join (select docid from Frequency where term = 'world') y
on x.docid = y.docid

select * from B where col_num = 3

select * from A where row_num = 2


select sum(value * BVal)
from A 
join (select row_num as BRow, col_num as BCol, value as BVal from B where col_num = 3) B
on A.col_num = B.BRow
where A.row_num = 2

select sum(A.count * B.count) from Frequency A
join Frequency B
on A.term = B.term
where A.docid = "10080_txt_crude" and B.docid = "17035_txt_earn"