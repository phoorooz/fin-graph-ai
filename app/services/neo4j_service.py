import os

from neo4j import GraphDatabase


class Neo4jService:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password),
        )

    def verify_connection(self):
        with self.driver.session() as session:
            result = session.run("RETURN 1 AS result")
            return result.single()["result"]

    def create_sample_graph(self):
        query = """
        MERGE (company:Company {name: "Microsoft"})

        MERGE (cloud:BusinessSegment {
            name: "Intelligent Cloud"
        })

        MERGE (productivity:BusinessSegment {
            name: "Productivity and Business Processes"
        })

        MERGE (azure:Product {
            name: "Azure"
        })

        MERGE (company)-[:HAS_SEGMENT]->(cloud)
        MERGE (company)-[:HAS_SEGMENT]->(productivity)
        MERGE (cloud)-[:HAS_PRODUCT]->(azure)

        RETURN company.name AS company,
               collect(DISTINCT cloud.name) AS segments,
               azure.name AS product
        """

        with self.driver.session() as session:
            result = session.run(query)
            return result.single().data()

    def create_financial_data(self):
        query = """
        MERGE (company:Company {name: "Microsoft"})

        MERGE (metric:FinancialMetric {name: "Revenue"})
        SET metric.value = 281.7,
            metric.unit = "billion USD",
            metric.growth = 15.0

        MERGE (period:ReportingPeriod {year: 2025})

        MERGE (company)-[:REPORTED]->(metric)
        MERGE (metric)-[:FOR_PERIOD]->(period)

        RETURN company.name AS company,
               metric.name AS metric,
               metric.value AS value,
               metric.unit AS unit,
               metric.growth AS growth,
               period.year AS year
        """

        with self.driver.session() as session:
            result = session.run(query)
            return result.single().data()

    def get_company_financials(self, company_name: str):
        query = """
        MATCH (company:Company {name: $company_name})
              -[:REPORTED]->(metric:FinancialMetric)
              -[:FOR_PERIOD]->(period:ReportingPeriod)

        RETURN company.name AS company,
               metric.name AS metric,
               metric.value AS value,
               metric.unit AS unit,
               metric.growth AS growth,
               period.year AS year
        ORDER BY period.year DESC
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                company_name=company_name,
            )

            return [record.data() for record in result]

    def get_metric(
        self,
        company_name: str,
        metric_name: str,
    ):
        query = """
        MATCH (company:Company {name: $company_name})
              -[:REPORTED]->(metric:FinancialMetric {
                  name: $metric_name
              })
              -[:FOR_PERIOD]->(period:ReportingPeriod)

        RETURN company.name AS company,
               metric.name AS metric,
               metric.value AS value,
               metric.unit AS unit,
               metric.growth AS growth,
               period.year AS year
        ORDER BY period.year DESC
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                company_name=company_name,
                metric_name=metric_name,
            )

            return [record.data() for record in result]

    def get_financial_graph(self, company_name: str):
        query = """
        MATCH (company:Company {name: $company_name})

        OPTIONAL MATCH (company)-[:REPORTED]->(metric:FinancialMetric)
              -[:FOR_PERIOD]->(period:ReportingPeriod)

        OPTIONAL MATCH (company)-[:HAS_SEGMENT]->(segment:BusinessSegment)
              -[:HAS_PRODUCT]->(product:Product)

        RETURN company.name AS company,
               collect(DISTINCT {
                   metric: metric.name,
                   value: metric.value,
                   unit: metric.unit,
                   growth: metric.growth,
                   year: period.year
               }) AS financial_metrics,
               collect(DISTINCT {
                   segment: segment.name,
                   product: product.name,
                   product_revenue: product.revenue,
                   product_revenue_unit: product.revenue_unit,
                   product_growth: product.growth
               }) AS business_relationships
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                company_name=company_name,
            )

            record = result.single()

            if not record:
                return {
                    "company": company_name,
                    "financial_metrics": [],
                    "business_relationships": [],
                }

            return record.data()

    def get_business_relationships(self, company_name: str):
        query = """
        MATCH (company:Company {name: $company_name})
              -[:HAS_SEGMENT]->(segment:BusinessSegment)
              -[:HAS_PRODUCT]->(product:Product)

        WITH company.name AS company,
             segment.name AS segment,
             product.name AS product,
             product.revenue AS revenue,
             product.revenue_unit AS revenue_unit,
             product.growth AS growth,
             product.revenue_note AS revenue_note

        RETURN company,
               segment,
               product,
               revenue,
               revenue_unit,
               growth,
               revenue_note
        ORDER BY product
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                company_name=company_name,
            )

            return [record.data() for record in result]

    def get_product_relationships(
        self,
        company_name: str,
        product_name: str,
    ):
        query = """
        MATCH (company:Company {name: $company_name})
              -[:HAS_SEGMENT]->(segment:BusinessSegment)
              -[:HAS_PRODUCT]->(product:Product {
                  name: $product_name
              })

        RETURN company.name AS company,
               segment.name AS segment,
               product.name AS product,
               product.revenue AS revenue,
               product.revenue_unit AS revenue_unit,
               product.growth AS growth,
               product.revenue_note AS revenue_note
        ORDER BY product
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                company_name=company_name,
                product_name=product_name,
            )

            return [record.data() for record in result]

    def close(self):
        self.driver.close()