-- Here I will create a fact table containing all the information, including dimension data.
-- This is not ideal, but in many BI projects it's rare to fully use all the features of relational databases.
-- That's mostly due to the rush to deliver dashboards quickly. These solutions often work fine in the short term (around 2 years),
-- but in the long term, they may lead to performance issues.
-- Although this approach is faster initially.

CREATE TABLE FACT.FT_TRANSPORT (
    ID INT PRIMARY KEY UNIQUE,
    BRANCH TEXT,
    DATE_TRANSP DATE,
    HOUR_TRANSP TIME,
    CATEGORY TEXT,
    PRODUCT TEXT,
    TTRASN INT,
    DEP_ORI TEXT,
    DEP_DEST TEXT,
    UNIT INT,
    USER_TRANSP TEXT
)
