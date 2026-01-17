{
    "name": "Lease Management",
    "summary": "Manage lease documents and alerts for expiry dates",
    "description": "Tracks lease expiries with visual alerts and attachments.",
    "author": "Noptechs",
    "website": "https://www.noptechs.com",
    "category": "Company Leases",
    "version": "0.1",
    "license": "OPL-1",
"depends": ["base", "mail","crm_extension",],
    "data": [
        "security/ir.model.access.csv",
        "views/lease_management_views.xml",
    ],
    "installable": True,
    "application": True,
}
