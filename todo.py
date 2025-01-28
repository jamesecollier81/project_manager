import curses
import json
from datetime import datetime, timedelta

# Nord theme colors
class NordColors:
    POLAR_NIGHT = {
        'nord0': 0,  # Dark gray
        'nord1': 1,  # Darker gray
        'nord2': 2,  # Medium gray
        'nord3': 3   # Light gray
    }
    
    SNOW_STORM = {
        'nord4': 4,  # Lightest gray
        'nord5': 5,  # Almost white
        'nord6': 6   # White
    }
    
    FROST = {
        'nord7': 7,  # Mint
        'nord8': 8,  # Ice blue
        'nord9': 9,  # Blue
        'nord10': 10 # Bright blue
    }
    
    AURORA = {
        'nord11': 11,  # Red
        'nord12': 12,  # Orange
        'nord13': 13,  # Yellow
        'nord14': 14,  # Green
        'nord15': 15   # Purple
    }

class Project:
    def __init__(self, name):
        self.name = name
        self.todos = []
        self.sort_by = 'description'  # or 'due_date'
        self.sort_reverse = False

    def sort_todos(self):
        if self.sort_by == 'description':
            self.todos.sort(key=lambda x: x['description'].lower(), reverse=self.sort_reverse)
        else:  # due_date
            self.todos.sort(key=lambda x: x.get('due_date', '9999-12-31'), reverse=self.sort_reverse)

class TodoManager:
    def __init__(self):
        self.projects = []
        self.active_window = 'projects'
        self.project_selection = 0
        self.todo_selection = 0
        self.load_data()

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
            'due_date': due_date
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

def init_nord_colors():
    # Polar Night
    curses.init_color(NordColors.POLAR_NIGHT['nord0'], 180, 204, 251)
    curses.init_color(NordColors.POLAR_NIGHT['nord1'], 231, 259, 322)
    curses.init_color(NordColors.POLAR_NIGHT['nord2'], 263, 298, 369)
    curses.init_color(NordColors.POLAR_NIGHT['nord3'], 298, 337, 416)
    
    # Snow Storm
    curses.init_color(NordColors.SNOW_STORM['nord4'], 847, 871, 914)
    curses.init_color(NordColors.SNOW_STORM['nord5'], 898, 914, 941)
    curses.init_color(NordColors.SNOW_STORM['nord6'], 925, 937, 957)
    
    # Frost
    curses.init_color(NordColors.FROST['nord7'], 561, 737, 733)
    curses.init_color(NordColors.FROST['nord8'], 533, 753, 816)
    curses.init_color(NordColors.FROST['nord9'], 506, 631, 757)
    curses.init_color(NordColors.FROST['nord10'], 369, 506, 675)
    
    # Aurora
    curses.init_color(NordColors.AURORA['nord11'], 749, 380, 416)
    curses.init_color(NordColors.AURORA['nord12'], 816, 529, 439)
    curses.init_color(NordColors.AURORA['nord13'], 922, 796, 545)
    curses.init_color(NordColors.AURORA['nord14'], 639, 745, 549)
    curses.init_color(NordColors.AURORA['nord15'], 706, 557, 678)

    # Modified color pairs to use nord0 (dark gray) as background
    curses.init_pair(1, NordColors.AURORA['nord14'], NordColors.POLAR_NIGHT['nord0'])  # Green on dark gray
    curses.init_pair(2, NordColors.AURORA['nord13'], NordColors.POLAR_NIGHT['nord0'])  # Yellow on dark gray
    curses.init_pair(3, NordColors.AURORA['nord11'], NordColors.POLAR_NIGHT['nord0'])  # Red on dark gray
    curses.init_pair(4, NordColors.FROST['nord8'], NordColors.POLAR_NIGHT['nord0'])    # Ice blue on dark gray
    curses.init_pair(5, NordColors.FROST['nord9'], NordColors.POLAR_NIGHT['nord0'])    # Blue on dark gray
    curses.init_pair(6, NordColors.SNOW_STORM['nord4'], NordColors.POLAR_NIGHT['nord0']) # Light gray on dark gray

def main(stdscr):
    curses.start_color()
    init_nord_colors()
    curses.curs_set(0)
    
    # Set background color for main screen
    stdscr.bkgd(' ', curses.color_pair(6))
    
    todo = TodoManager()
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
        commands = "[TAB] Switch window | [a] Add | [d] Delete | [e] Edit | [space] Toggle todo | [s] Sort | [q] Quit"
        stdscr.addstr(2, 0, commands)

        # Project window
        project_win.addstr(0, 2, "Projects")
        for i, project in enumerate(todo.projects):
            style = curses.A_REVERSE if i == todo.project_selection and todo.active_window == 'projects' else curses.A_NORMAL
            project_win.addstr(i+1, 2, f"• {project.name}", style)

        # Todo window
        todo_win.addstr(0, 2, f"Todos - {todo.projects[todo.project_selection].name if todo.projects else 'No Project'}")
        if todo.projects:
            todos = todo.projects[todo.project_selection].todos
            for i, task in enumerate(todos):
                prefix = "✓ " if task['completed'] else "☐ "
                style = curses.color_pair(1) if task['completed'] else curses.A_NORMAL
                if i == todo.todo_selection and todo.active_window == 'todos':
                    style |= curses.A_REVERSE
                
                due_date_str = f"Due: {task.get('due_date', 'No due date')}"
                task_str = f"{prefix}{task['description']} ({due_date_str})"
                todo_win.addstr(i+1, 2, task_str, style)
            project = todo.projects[todo.project_selection]
            sort_indicator = "↑" if not project.sort_reverse else "↓"
            header = f"Todos - {project.name} (Sorted by: {project.sort_by} {sort_indicator})"
        else:
            header = "Todos - No Project"
        todo_win.addstr(0, 2, header)

        stdscr.refresh()
        project_win.refresh()
        todo_win.refresh()

        key = stdscr.getch()
        if key == ord('q'):
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

if __name__ == "__main__":
    curses.wrapper(main)