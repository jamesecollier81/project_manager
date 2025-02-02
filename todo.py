import curses
import json
import os
import shutil
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
        curses.init_color(0, 157, 165, 180)   # Background
        curses.init_color(1, 1000, 1000, 1000)  # Brightened default text
        curses.init_color(2, 552, 823, 552)   # Green
        curses.init_color(3, 913, 725, 525)   # Orange
        curses.init_color(4, 898, 450, 450)   # Red
        curses.init_color(5, 400, 627, 913)   # Blue
        curses.init_color(6, 788, 572, 933)   # Purple
        curses.init_color(7, 552, 784, 745)   # Cyan
        
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

class Project:
    def __init__(self, name):
        self.name = name
        self.todos = []
        self.sort_by = 'description'
        self.sort_reverse = False

    def sort_todos(self):
        sort_keys = {
            'description': lambda x: (x['completed'], x['description'].lower()),
            'due_date': lambda x: (x['completed'], x['due_date'] or '9999-12-31'),
            'priority': lambda x: (x['completed'], {'high': 0, 'medium': 1, 'low': 2}[x.get('priority', 'medium')]),
            'created': lambda x: (x['completed'], x['created_at'])
        }
        
        if self.sort_by not in sort_keys:
            self.sort_by = 'due_date'
            
        self.todos.sort(key=sort_keys[self.sort_by], reverse=self.sort_reverse)

class TodoManager:
    def __init__(self):
        self.projects = []
        self.active_window = 'projects'
        self.project_selection = 0
        self.todo_selection = 0
        self.show_completed = True
        self.backup_dir = 'todo_backups'
        self.ensure_backup_directory()
        self.load_data()
        self.theme_manager = ThemeManager()

    def ensure_backup_directory(self):
        """Create backup directory if it doesn't exist"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self):
        """Create a backup of the current projects.json file"""
        if os.path.exists('projects.json'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(self.backup_dir, f'projects_{timestamp}.json')
            shutil.copy2('projects.json', backup_path)
            
            # Keep only the last 10 backups
            backups = sorted([f for f in os.listdir(self.backup_dir) if f.startswith('projects_')])
            while len(backups) > 10:
                os.remove(os.path.join(self.backup_dir, backups.pop(0)))

    def load_data(self):
        try:
            with open('projects.json', 'r') as f:
                data = json.load(f)
                self.projects = [Project(p['name']) for p in data]
                for proj, saved_proj in zip(self.projects, data):
                    proj.todos = saved_proj['todos']
        except FileNotFoundError:
            self.projects = [Project("Default")]

    def save_data(self):
        """Save data with automatic backup"""
        self.create_backup()  # Create backup before saving
        data = [{'name': p.name, 'todos': p.todos} for p in self.projects]
        with open('projects.json', 'w') as f:
            json.dump(data, f)

    def get_visible_todos(self):
        if not self.projects:
            return []
        todos = self.projects[self.project_selection].todos
        if not self.show_completed:
            todos = [todo for todo in todos if not todo['completed']]
        return todos

    def toggle_completed_visibility(self):
        self.show_completed = not self.show_completed
        visible_todos = self.get_visible_todos()
        if self.todo_selection >= len(visible_todos):
            self.todo_selection = max(0, len(visible_todos) - 1)

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
            'priority': 'medium'
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

    def delete_project(self, stdscr=None):
        if not self.projects:
            return False
        
        if stdscr:
            max_y, max_x = stdscr.getmaxyx()
            project_name = self.projects[self.project_selection].name
            stdscr.addstr(max_y-2, 0, f"Are you sure you want to delete project '{project_name}'? (y/n): ")
            stdscr.clrtoeol()
            stdscr.refresh()
            
            while True:
                confirm = stdscr.getch()
                if confirm == ord('y'):
                    self.create_backup()  # Create backup before deletion
                    del self.projects[self.project_selection]
                    if self.project_selection >= len(self.projects):
                        self.project_selection = max(0, len(self.projects) - 1)
                    self.save_data()
                    return True
                elif confirm == ord('n'):
                    return False
        return False

    def edit_todo(self, new_description=None, new_due_date=None):
        if not self.projects or not self.projects[self.project_selection].todos:
            return
        todo = self.projects[self.project_selection].todos[self.todo_selection]
        if new_description:
            todo['description'] = new_description
        if new_due_date is not None:
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

    def restore_backup(self, backup_file=None):
        """Restore from a backup file"""
        if backup_file is None:
            # Get the most recent backup
            backups = sorted([f for f in os.listdir(self.backup_dir) if f.startswith('projects_')])
            if not backups:
                return False
            backup_file = backups[-1]
        
        backup_path = os.path.join(self.backup_dir, backup_file)
        if os.path.exists(backup_path):
            # Create a backup of current state before restoring
            self.create_backup()
            # Restore from backup
            shutil.copy2(backup_path, 'projects.json')
            self.load_data()
            return True
        return False

    def list_backups(self):
        """Return a list of available backups"""
        if not os.path.exists(self.backup_dir):
            return []
        return sorted([f for f in os.listdir(self.backup_dir) if f.startswith('projects_')])

def parse_due_date(date_str):
    try:
        if not date_str:
            return None
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

def get_todo_style(todo):
    if todo['completed']:
        return curses.color_pair(1)
    
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
    prefix = "✓ " if todo['completed'] else "☐ "
    
    due_date_str = ""
    if todo.get('due_date'):
        try:
            due_date = datetime.strptime(todo['due_date'], "%Y-%m-%d").date()
            today = datetime.now().date()
            days_until_due = (due_date - today).days
            
            if not todo['completed']:
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
    
    return f"{prefix}{todo['description']}{due_date_str}"

def main(stdscr):
    curses.start_color()
    curses.curs_set(0)
    
    todo = TodoManager()
    todo.theme_manager.init_nord_theme()
    
    max_y, max_x = stdscr.getmaxyx()
    
    project_win = curses.newwin(max_y-3, max_x//3, 3, 0)
    todo_win = curses.newwin(max_y-3, (2*max_x//3)-1, 3, max_x//3+1)
    
    project_win.bkgd(' ', curses.color_pair(6))
    todo_win.bkgd(' ', curses.color_pair(6))    

    while True:
        stdscr.clear()
        project_win.clear()
        todo_win.clear()

        project_win.border()
        todo_win.border()

        stdscr.addstr(0, 0, "PROJECT MANAGER", curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * max_x)
        commands = "[TAB] Switch window | [a] Add | [d] Delete | [e] Edit | [space] Toggle todo | [s] Sort | [h] Hide/Show completed | [t] Theme | [r] Restore backup | [q] Quit"
        stdscr.addstr(2, 0, commands)

        project_win.addstr(0, 2, "Projects")
        for i, project in enumerate(todo.projects):
            style = curses.A_REVERSE if i == todo.project_selection and todo.active_window == 'projects' else curses.A_NORMAL
            project_win.addstr(i+1, 2, f"• {project.name}", style)

        todo_win.addstr(0, 2, f"Todos - {todo.projects[todo.project_selection].name if todo.projects else 'No Project'}")
        if todo.projects:
            visible_todos = todo.get_visible_todos()
            completed_count = len([t for t in todo.projects[todo.project_selection].todos if t['completed']])
            total_count = len(todo.projects[todo.project_selection].todos)
            
            header = f"Todos - {todo.projects[todo.project_selection].name} ({completed_count}/{total_count} completed)"
            if not todo.show_completed:
                header += " (hiding completed)"
            todo_win.addstr(0, 2, header)

            for i, task in enumerate(visible_todos):
                style = get_todo_style(task)
                if i == todo.todo_selection and todo.active_window == 'todos':
                    style |= curses.A_REVERSE
                
                display_str = format_todo_display(task)
                todo_win.addstr(i+1, 2, display_str, style)

        stdscr.refresh()
        project_win.refresh()
        todo_win.refresh()

        key = stdscr.getch()
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
                stdscr.clrtoeol()
                name = stdscr.getstr().decode('utf-8')
                if name:
                    todo.add_project(name)
            else:
                if todo.projects:
                    stdscr.addstr(max_y-2, 0, "Enter todo description: ")
                    stdscr.clrtoeol()
                    description = stdscr.getstr().decode('utf-8')
                    stdscr.addstr(max_y-1, 0, "Enter due date (YYYY-MM-DD/today/tomorrow/next week, or leave empty): ")
                    stdscr.clrtoeol()
                    due_date_str = stdscr.getstr().decode('utf-8')
                    if description:
                        due_date = parse_due_date(due_date_str) if due_date_str else None
                        todo.add_todo(description, due_date)
            
            curses.noecho()
            curses.curs_set(0)
        elif key == ord('d'):
            if todo.active_window == 'projects':
                todo.delete_project(stdscr)
            else:
                todo.delete_todo()
        elif key == ord(' '):
            if todo.active_window == 'todos':
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
                visible_todos = todo.get_visible_todos()
                todo.todo_selection = min(len(visible_todos) - 1, todo.todo_selection + 1)
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
        elif key == ord('r'):  # Restore backup functionality
            if todo.active_window == 'projects':
                backups = todo.list_backups()
                if backups:
                    curses.echo()
                    curses.curs_set(1)
                    stdscr.addstr(max_y-2, 0, "Enter backup number to restore (0 for most recent): ")
                    stdscr.clrtoeol()
                    try:
                        choice = stdscr.getstr().decode('utf-8')
                        if choice.strip() == '':
                            todo.restore_backup()
                        else:
                            backup_idx = int(choice)
                            if 0 <= backup_idx < len(backups):
                                todo.restore_backup(backups[-(backup_idx+1)])
                    except ValueError:
                        pass
                    curses.noecho()
                    curses.curs_set(0)

if __name__ == "__main__":
    curses.wrapper(main)                   
