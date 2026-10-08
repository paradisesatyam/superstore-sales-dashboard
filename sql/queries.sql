-- Revenue and profit by year
SELECT year, ROUND(SUM(sales), 2) AS revenue, ROUND(SUM(profit), 2) AS profit
FROM orders
GROUP BY year
ORDER BY year;

-- Sub-categories that lose money overall
SELECT category, sub_category, ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY category, sub_category
HAVING total_profit < 0
ORDER BY total_profit;

-- Top 10 customers by revenue
SELECT customer_id, customer_name, ROUND(SUM(sales), 2) AS revenue
FROM orders
GROUP BY customer_id, customer_name
ORDER BY revenue DESC
LIMIT 10;

-- Month-over-month sales growth (window function)
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m-01') AS month, SUM(sales) AS sales
    FROM orders
    GROUP BY month
)
SELECT month, ROUND(sales, 2) AS sales,
       ROUND((sales - LAG(sales) OVER (ORDER BY month)) / LAG(sales) OVER (ORDER BY month) * 100, 1) AS growth_pct
FROM monthly;

-- Does discounting hurt profit?
SELECT discount, COUNT(*) AS lines, ROUND(AVG(profit), 2) AS avg_profit
FROM orders
GROUP BY discount
ORDER BY discount;
