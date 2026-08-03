# Odoo 18 Community: Aaqify Sale Discount Approval Module

An automated approval workflow module for **Odoo 18 Community Edition**. This custom addon enables businesses to define maximum discount thresholds per company. Whenever a sales order exceeds the set discount percentage, automatic activities (tasks) are generated for specified approver users in the order's chatter.

---

<img width="1600" height="751" alt="image" src="https://github.com/user-attachments/assets/a183e489-45e9-4629-a3d4-ad207b9d8589" />

---
## 📌 Features

* **Configurable Rules:** Define rule names, discount percentage thresholds, approver users, and companies.
* **Multi-Company Support:** Associate approval rules with specific companies in multi-company environments.
* **Multi-User Assignment (`many2many`):** Assign multiple approvers per rule simultaneously.
* **Automated Activity Creation:** Generates a **To-Do** activity directly in the Sales Order chatter upon confirmation.
* **Duplicate Prevention:** Prevents creating duplicate open activities for the same order and user.
* **Native Integration:** Located seamlessly under `Sales > Configuration > Sale dist. Approval`.

---

## 📂 Module Architecture

```text
sale_discount_approval/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── sale_discount_approval.py
│   └── sale_order.py
├── views/
│   └── sale_discount_approval_view.xml
└── security/
    └── ir.model.access.csv
