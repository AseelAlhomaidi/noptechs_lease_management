{
    "name": "Lease Management",
    "summary": "Manage lease documents and alerts for expiry dates",
    "description": "Tracks lease expiries with visual alerts and attachments.",
    "author": "Noptechs",
    "website": "https://www.noptechs.com",
    "category": "Company Leases",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
"depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/lease_management_views.xml",
    ],
    "installable": True,
    "application": True,
}
