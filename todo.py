import curses
import json
from datetime import datetime, timedelta

class ThemeManager:
    def __init__(self):
        self.current_theme = "nord"
        
    def init_nord_theme(self):
        curses.init_color(0, 100, 110, 140)  # Background
        curses.init_color(1, 180, 190, 210)
        curses.init_color(2, 220, 230, 250)
        curses.init_color(3, 260, 270, 290)
        curses.init_color(4, 900, 910, 930)  # Brightened default text color
        curses.init_color(5, 940, 950, 960)
        curses.init_color(6, 970, 980, 990)
        curses.init_color(7, 600, 800, 780)
        curses.init_color(8, 580, 820, 900)
        curses.init_color(9, 520, 680, 850)
        curses.init_color(10, 400, 600, 800)
        curses.init_color(11, 850, 400, 400)
        curses.init_color(12, 900, 600, 450)
        curses.init_color(13, 980, 850, 500)
        curses.init_color(14, 650, 850, 550)
        curses.init_color(15, 800, 600, 750)

        curses.init_pair(1, 14, 0)  # Green for completed
        curses.init_pair(2, 13, 0)  # Yellow for in progress
        curses.init_pair(3, 11, 0)  # Red for overdue
        curses.init_pair(4, 8, 0)   # Ice blue for headers
        curses.init_pair(5, 9, 0)   # Blue for selection
        curses.init_pair(6, 15, 0)  # Changed to bright purple-white for better visibility

    def init_atom_dark_theme(self):
        # Atom One Dark colors
        curses.init_color(0, 157, 165, 180)   # Background #282C34
        curses.init_color(1, 1000, 1000, 1000)  # Brightened default text to pure white
        curses.init_color(2, 552, 823, 552)   # Green #8DC28D
        curses.init_color(3, 913, 725, 525)   # Orange #E9B984
        curses.init_color(4, 898, 450, 450)   # Red #E57373
        curses.init_color(5, 400, 627, 913)   # Blue #66A0E9
        curses.init_color(6, 788, 572, 933)   # Purple #C992EE
        curses.init_color(7, 552, 784, 745)   # Cyan #8DC8BE
        
        curses.init_pair(1, 2, 0)   # Green for completed
        curses.init_pair(2, 3, 0)   # Orange for in progress
        curses.init_pair(3, 4, 0)   # Red for overdue
        curses.init_pair(4, 5, 0)   # Blue for headers
        curses.init_pair(5, 6, 0)   # Purple for selection
        curses.init_pair(6, 1, 0)   # Pure white for default text
        curses.init_pair(7, 6, 0)   # Purple for high priority
        curses.init_pair(8, 7, 0)   # Cyan for tags

    def init_matrix_theme(self):
        curses.init_color(0, 0, 0, 0)         # Pure black
        curses.init_color(1, 0, 1000, 0)      # Bright matrix green
        curses.init_color(2, 0, 800, 0)       # Medium matrix green
        curses.init_color(3, 0, 600, 0)       # Dark matrix green
        curses.init_color(4, 0, 400, 0)       # Darker matrix green
        
        curses.init_pair(1, 1, 0)   # Bright green for completed
        curses.init_pair(2, 2, 0)   # Medium green for in progress
        curses.init_pair(3, 3, 0)   # Dark green for overdue
        curses.init_pair(4, 1, 0)   # Bright green for headers
        curses.init_pair(5, 1, 0)   # Bright green for selection
        curses.init_pair(6, 1, 0)   # Changed to bright green for default text
        curses.init_pair(7, 1, 0)   # Bright green for high priority
        curses.init_pair(8, 4, 0)   # Darker green for tags

    def toggle_theme(self):
        themes = ["nord", "atom-dark", "matrix"]
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.current_theme = themes[next_index]
        
        if self.current_theme == "nord":
            self.init_nord_theme()
        elif self.current_theme == "atom-dark":
            self.init_atom_dark_theme()
        else:
            self.init_matrix_theme()

class Todo:
    def __init__(self, description, due_date=None):
        self.description = description
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.due_date = due_date
        self.priority = "medium"  # New: priority level
        self.tags = []           # New: tags for categorization
        self.notes = ""          # New: additional notes
        self.reminder = None     # New: reminder date/time
        
class Project:
    def __init__(self, name):
        self.name = name
        self.todos = []
        self.sort_by = 'description'
        self.sort_reverse = False
        self.filter_completed = False  # New: option to hide completed tasks
        self.filter_tags = []         # New: filter by tags
        self.view_mode = 'all'        # New: view mode (all, today, week)

    def sort_todos(self):
        sort_keys = {
        'description': lambda x: (x['completed'], x['description'].lower()),
        'due_date': lambda x: (x['completed'], x['due_date'] or '9999-12-31'),
        'priority': lambda x: (x['completed'], {'high': 0, 'medium': 1, 'low': 2}[x.get('priority', 'medium')]),
        'created': lambda x: (x['completed'], x['created_at'])
    }
    
        if self.sort_by not in sort_keys:
            self.sort_by = 'description'  # Default sort method
            
        self.todos.sort(key=sort_keys[self.sort_by], reverse=self.sort_reverse)

    def edit_todo(self, new_description=None, new_due_date=None):
        if not self.projects or not self.projects[self.project_selection].todos:
            return
        todo = self.projects[self.project_selection].todos[self.todo_selection]
        if new_description:
            todo['description'] = new_description
        if new_due_date is not None:
            todo['due_date'] = new_due_date if new_due_date else None
        self.save_data()
        self.projects[self.project_selection].sort_todos()

class TodoManager:
    def __init__(self):
        self.projects = []
        self.active_window = 'projects'
        self.project_selection = 0
        self.todo_selection = 0
        self.show_completed = False
        self.load_data()
        self.theme_manager = ThemeManager()

    def load_data(self):
        try:
            with open('projects.json', 'r') as f:
                data = json.load(f)
                self.projects = [Project(p['name']) for p in data]
                for proj, saved_proj in zip(self.projects, data):
                    proj.todos = saved_proj['todos']
        except FileNotFoundError:
            self.projects = [Project("Default")]

    def get_visible_todos(self):
        if not self.projects:
            return []
        todos = self.projects[self.project_selection].todos
        
        # Apply completed filter if needed
        if not self.show_completed:
            todos = [todo for todo in todos if not todo['completed']]    
        return todos

    def toggle_completed_visibility(self):
        """Toggle whether completed tasks are shown"""
        self.show_completed = not self.show_completed
        # Adjust selection if current todo is now hidden
        visible_todos = self.get_visible_todos()
        if self.todo_selection >= len(visible_todos):
            self.todo_selection = max(0, len(visible_todos) - 1)

    def save_data(self):
        data = [{'name': p.name, 'todos': p.todos} for p in self.projects]
        with open('projects.json', 'w') as f:
            json.dump(data, f)

    def add_project(self, name):
        self.projects.append(Project(name))
        self.save_data()

    def add_todo(self, description, due_date=None):
        if not self.projects:
            return
        todo = {
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'due_date': due_date,
            'priority': 'medium'  # Default priority
        }
        self.projects[self.project_selection].todos.append(todo)
        self.save_data()

    def toggle_todo(self):
        if not self.projects or not self.projects[self.project_selection].todos:
            return
        todos = self.projects[self.project_selection].todos
        todos[self.todo_selection]['completed'] = not todos[self.todo_selection]['completed']
        self.save_data()

    def delete_todo(self):
        if not self.projects or not self.projects[self.project_selection].todos:
            return
        todos = self.projects[self.project_selection].todos
        del todos[self.todo_selection]
        if self.todo_selection >= len(todos):
            self.todo_selection = max(0, len(todos) - 1)
        self.save_data()

    def delete_project(self):
        if not self.projects:
            return
        del self.projects[self.project_selection]
        if self.project_selection >= len(self.projects):
            self.project_selection = max(0, len(self.projects) - 1)
        self.save_data()
        
    def edit_todo(self, new_description=None, new_due_date=None):
        if not self.projects or not self.projects[self.project_selection].todos:
            return
        todo = self.projects[self.project_selection].todos[self.todo_selection]
        if new_description:
            todo['description'] = new_description
        if new_due_date is not None:  # Allow empty string to clear due date
            todo['due_date'] = new_due_date if new_due_date else None
        self.projects[self.project_selection].sort_todos()
        self.save_data()

    def toggle_sort(self, sort_by):
        if not self.projects:
            return
        project = self.projects[self.project_selection]
        if project.sort_by == sort_by:
            project.sort_reverse = not project.sort_reverse
        else:
            project.sort_by = sort_by
            project.sort_reverse = False
        project.sort_todos()

def parse_due_date(date_str):
    try:
        if date_str.lower() == 'today':
            return datetime.now().strftime("%Y-%m-%d")
        elif date_str.lower() == 'tomorrow':
            return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_str.lower() == 'next week':
            return (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%Y-%m-%d")
    except ValueError:
        return None

def get_todo_display_style(todo):
    """Enhanced styling based on todo status and priority"""
    if todo.completed:
        return curses.color_pair(1)  # Green for completed
    if todo.due_date:
        due_date = datetime.strptime(todo.due_date, "%Y-%m-%d")
        if due_date.date() < datetime.now().date():
            return curses.color_pair(3)  # Red for overdue
    if todo.priority == "high":
        return curses.color_pair(7)  # Purple for high priority
    return curses.color_pair(6)  # Default style

def get_visible_todos(self):
        """Returns filtered list of todos based on current settings"""
        if not self.projects:
            return []
        todos = self.projects[self.project_selection].todos
        if not self.show_completed:
            todos = [todo for todo in todos if not todo['completed']]
        return todos

def get_todo_style(todo):
    """Get the appropriate color style for a todo item"""
    if todo['completed']:
        return curses.color_pair(1)  # Green for completed
    
    if todo.get('due_date'):
        try:
            due_date = datetime.strptime(todo['due_date'], "%Y-%m-%d").date()
            today = datetime.now().date()
            days_until_due = (due_date - today).days
            
            if days_until_due < 0:
                return curses.color_pair(3)  # Red for overdue
            elif days_until_due <= 2:
                return curses.color_pair(2)  # Yellow for urgent
        except ValueError:
            pass
    
    return curses.color_pair(6)  # Default style

def format_todo_display(todo):
    """Format todo item with visual indicators"""
    # Status indicator
    prefix = "✓ " if todo['completed'] else "☐ "
    
    # Due date formatting with warning
    due_date_str = ""
    if todo.get('due_date'):
        try:
            due_date = datetime.strptime(todo['due_date'], "%Y-%m-%d").date()
            today = datetime.now().date()
            days_until_due = (due_date - today).days
            
            if not todo['completed']:  # Only show warnings for incomplete tasks
                if days_until_due < 0:
                    due_date_str = f" ⚠ Overdue by {abs(days_until_due)} days"
                elif days_until_due == 0:
                    due_date_str = " ⚠ Due today!"
                elif days_until_due <= 2:
                    due_date_str = f" ⚠ Due in {days_until_due} days"
                else:
                    due_date_str = f" ({todo['due_date']})"
            else:
                due_date_str = f" (Done: {todo['due_date']})"
        except ValueError:
            due_date_str = f" ({todo['due_date']})"
    
    # Just combine status, description, and due date (no priority markers)
    return f"{prefix}{todo['description']}{due_date_str}"

def main(stdscr):
    curses.start_color()
    curses.curs_set(0)
    
    todo = TodoManager()  # Create TodoManager first
    todo.theme_manager.init_nord_theme()  # Then initialize theme
    
    max_y, max_x = stdscr.getmaxyx()
    
    # Create windows with Nord theme background
    project_win = curses.newwin(max_y-3, max_x//3, 3, 0)
    todo_win = curses.newwin(max_y-3, (2*max_x//3)-1, 3, max_x//3+1)
    
    # Set background for both windows
    project_win.bkgd(' ', curses.color_pair(6))
    todo_win.bkgd(' ', curses.color_pair(6))    

    while True:
        stdscr.clear()
        project_win.clear()
        todo_win.clear()

        # Draw borders
        project_win.border()
        todo_win.border()

        # Headers
        stdscr.addstr(0, 0, "PROJECT MANAGER", curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * max_x)
        commands = "[TAB] Switch window | [a] Add | [d] Delete | [e] Edit | [space] Toggle todo | [s] Sort | [h] Hide/Show completed | [t] Switch theme | [q] Quit"
        stdscr.addstr(2, 0, commands)

        # Project window
        project_win.addstr(0, 2, "Projects")
        for i, project in enumerate(todo.projects):
            style = curses.A_REVERSE if i == todo.project_selection and todo.active_window == 'projects' else curses.A_NORMAL
            project_win.addstr(i+1, 2, f"• {project.name}", style)

        # Todo window
        todo_win.addstr(0, 2, f"Todos - {todo.projects[todo.project_selection].name if todo.projects else 'No Project'}")
        if todo.projects:
            visible_todos = todo.get_visible_todos()
            completed_count = len([t for t in todo.projects[todo.project_selection].todos if t['completed']])
            total_count = len(todo.projects[todo.project_selection].todos)
            
            # Update header to show task counts
            header = f"Todos - {todo.projects[todo.project_selection].name} ({completed_count}/{total_count} completed)"
            if not todo.show_completed:
                header += " (hiding completed)"
            todo_win.addstr(0, 2, header)

            # Display todos with enhanced formatting
            for i, task in enumerate(visible_todos):
                style = get_todo_style(task)
                if i == todo.todo_selection and todo.active_window == 'todos':
                    style |= curses.A_REVERSE
                
                display_str = format_todo_display(task)
                todo_win.addstr(i+1, 2, display_str, style)

        stdscr.refresh()
        project_win.refresh()
        todo_win.refresh()

        key = stdscr.getch() #key handling
        if key == ord('h'):
            todo.toggle_completed_visibility()
        elif key == ord('q'):
            break
        elif key == ord('\t'):
            todo.active_window = 'todos' if todo.active_window == 'projects' else 'projects'
        elif key == ord('a'):
            curses.echo()
            curses.curs_set(1)
            
            if todo.active_window == 'projects':
                stdscr.addstr(max_y-2, 0, "Enter project name: ")
                name = stdscr.getstr().decode('utf-8')
                if name:
                    todo.add_project(name)
            else:
                if todo.projects:
                    stdscr.addstr(max_y-2, 0, "Enter todo description: ")
                    description = stdscr.getstr().decode('utf-8')
                    stdscr.addstr(max_y-1, 0, "Enter due date (YYYY-MM-DD/today/tomorrow/next week, or leave empty): ")
                    due_date_str = stdscr.getstr().decode('utf-8')
                    if description:
                        due_date = parse_due_date(due_date_str) if due_date_str else None
                        todo.add_todo(description, due_date)
            
            curses.noecho()
            curses.curs_set(0)
        elif key == ord('d'):
            if todo.active_window == 'projects':
                todo.delete_project()
            else:
                todo.delete_todo()
        elif key == ord(' ') and todo.active_window == 'todos':
            todo.toggle_todo()
        elif key == curses.KEY_UP:
            if todo.active_window == 'projects':
                todo.project_selection = max(0, todo.project_selection - 1)
            else:
                todo.todo_selection = max(0, todo.todo_selection - 1)
        elif key == curses.KEY_DOWN:
            if todo.active_window == 'projects':
                todo.project_selection = min(len(todo.projects) - 1, todo.project_selection + 1)
            else:
                todos = todo.projects[todo.project_selection].todos if todo.projects else []
                todo.todo_selection = min(len(todos) - 1, todo.todo_selection + 1)
                
        elif key == ord('p') and todo.active_window == 'todos':
            if todo.projects and todo.projects[todo.project_selection].todos:
                stdscr.addstr(max_y-2, 0, "Set priority - (h)igh, (m)edium, (l)ow: ")
                stdscr.clrtoeol()
                priority_key = stdscr.getch()
                
                if priority_key in [ord('h'), ord('m'), ord('l')]:
                    current_todo = todo.projects[todo.project_selection].todos[todo.todo_selection]
                    if priority_key == ord('h'):
                        current_todo['priority'] = 'high'
                    elif priority_key == ord('m'):
                        current_todo['priority'] = 'medium'
                    else:
                        current_todo['priority'] = 'low'
                    todo.save_data()  # Call save_data() on the TodoManager instance

        elif key == ord('e') and todo.active_window == 'todos':
            if todo.projects and todo.projects[todo.project_selection].todos:
                curses.echo()
                curses.curs_set(1)
                current_todo = todo.projects[todo.project_selection].todos[todo.todo_selection]
                
                stdscr.addstr(max_y-2, 0, "Edit description (leave empty to keep current): ")
                stdscr.clrtoeol()
                new_desc = stdscr.getstr().decode('utf-8')
                
                stdscr.addstr(max_y-1, 0, "Edit due date (YYYY-MM-DD/today/tomorrow/next week, or leave empty to keep current): ")
                stdscr.clrtoeol()
                new_date_str = stdscr.getstr().decode('utf-8')
                
                if new_desc or new_date_str:
                    new_date = parse_due_date(new_date_str) if new_date_str else current_todo.get('due_date')
                    todo.edit_todo(
                        new_description=new_desc if new_desc else current_todo['description'],
                        new_due_date=new_date
                    )
                
                curses.noecho()
                curses.curs_set(0)
        elif key == ord('s') and todo.active_window == 'todos':
            stdscr.addstr(max_y-2, 0, "Sort by (n)ame or (d)ue date?: ")
            stdscr.clrtoeol()
            sort_key = stdscr.getch()
            if sort_key == ord('n'):
                todo.toggle_sort('description')
            elif sort_key == ord('d'):
                todo.toggle_sort('due_date')
        elif key == ord('t'):
            todo.theme_manager.toggle_theme()
pass

if __name__ == "__main__":
    curses.wrapper(main)
