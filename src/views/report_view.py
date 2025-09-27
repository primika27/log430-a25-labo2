"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param

def show_highest_spending_users():
    """ Show report of highest spending users """
    from queries.read_order import get_highest_spending_users
    from queries.read_user import get_user_by_id
    
    rows = []
    for user_id, total in get_highest_spending_users():
        user = get_user_by_id(int(user_id))
        name = user.get("name", f"Utilisateur {user_id}")
        rows.append(f"<tr><td>{name}</td><td>${total:.2f}</td></tr>")
    
    table = "\n".join(rows) if rows else "<tr><td colspan=2>Aucune donnée</td></tr>"
    return get_template(f"""
        <h2>Les plus gros acheteurs</h2>
        <table class="table">
            <tr><th>Utilisateur</th><th>Total dépensé</th></tr>
            {table}
        </table>
    """)

def show_best_sellers():
    """ Show report of best selling products """
    return get_template("<h2>Les articles les plus vendus</h2><p>(TODO: Liste avec nom, total vendu)</p>")