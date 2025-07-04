#import needed libraries
import curses
import json
import os
import shutil
from datetime import datetime, timedelta
import copy
from typing import List, Set, Optional

class UndoManager:
    def __init__(self, max_history: int = 50):
        self.undo_stack = []
        self.redo_stack = []
        self.max_history = max_history
    
    def push_state(self, state):
        """Save current state to undo stack"""
        self.undo_stack.append(copy.deepcopy(state))
        self.redo_stack.clear()  # Clear redo stack when new action is performed
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
    
    def undo(self, current_state) -> Optional[dict]:
        """Undo last action"""
        if self.undo_stack:
            self.redo_stack.append(copy.deepcopy(current_state))
            return self.undo_stack.pop()
        return None
    
    def redo(self, current_state) -> Optional[dict]:
        """Redo last undone action"""
        if self.redo_stack:
            self.undo_stack.append(copy.deepcopy(current_state))
            return self.redo_stack.pop()
        return None
    
#curent themes: Nord, Atom Dark, and Matrix(dos like)
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
    
    def init_dracula_theme(self):
        curses.init_color(0, 157, 158, 172)   # Background
        curses.init_color(1, 980, 976, 925)   # White
        curses.init_color(2, 556, 972, 509)   # Green
        curses.init_color(3, 980, 647, 529)   # Orange
        curses.init_color(4, 980, 474, 509)   # Pink
        curses.init_color(5, 388, 611, 996)   # Purple
        curses.init_color(6, 733, 737, 956)   # Comment
        curses.init_color(7, 964, 890, 690)   # Yellow

        curses.init_pair(1, 2, 0)   # Green for completed
        curses.init_pair(2, 7, 0)   # Yellow for in progress
        curses.init_pair(3, 4, 0)   # Pink for overdue
        curses.init_pair(4, 5, 0)   # Purple for headers
        curses.init_pair(5, 3, 0)   # Orange for selection
        curses.init_pair(6, 1, 0)   # White for default text
        curses.init_pair(7, 4, 0)   # Pink for high priority
        curses.init_pair(8, 6, 0)   # Comment color for tags

    def init_longhorns_theme(self):
        # Texas Longhorns color values
        curses.init_color(0, 51, 63, 78)      # Background #0D1117
        curses.init_color(1, 788, 831, 866)   # Foreground #C9D1DC
        curses.init_color(2, 600, 600, 600)   # Silver #999999
        curses.init_color(3, 960, 784, 360)   # Yellow #F6C862
        curses.init_color(4, 960, 549, 219)   # Orange #F68D38
        curses.init_color(5, 474, 690, 960)   # Purple #79B0F5
        curses.init_color(6, 360, 600, 960)   # Accent Blue #5C99F5
        curses.init_color(7, 749, 341, 0)   # burnt orange #BF5700

        # Define color pairs
        curses.init_pair(1, 2, 0)   # Blue for completed
        curses.init_pair(2, 3, 0)   # Yellow for in progress
        curses.init_pair(3, 7, 0)   # Red for overdue
        curses.init_pair(4, 5, 0)   # Purple for headers
        curses.init_pair(5, 4, 0)   # Orange for selection
        curses.init_pair(6, 1, 0)   # Default text color
        curses.init_pair(7, 6, 0)   # Accent Blue for high priority
        curses.init_pair(8, 2, 0)   # Blue for tags

    def toggle_theme(self):
        themes = ["nord", "atom-dark", "matrix", "dracula", "longhorns"]
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.current_theme = themes[next_index]
        
        if self.current_theme == "nord":
            self.init_nord_theme()
        elif self.current_theme == "atom-dark":
            self.init_atom_dark_theme()
        elif self.current_theme == "matrix":
            self.init_matrix_theme()
        elif self.current_theme == "dracula":
            self.init_dracula_theme()
        else:
            self.init_longhorns_theme()

class Project:
    def __init__(self, name):
        self.name = name
        self.todos = []
        self.sort_by = 'due_date'  # Changed default sort to due_date
        self.sort_reverse = False
        self.categories: Set[str] = set()

    def sort_todos(self):
        def get_sort_key(todo):
            completed = todo['completed']
            if self.sort_by == 'due_date':
                due_date = todo.get('due_date') or '9999-12-31'
                return (completed, due_date)
            elif self.sort_by == 'description':
                return (completed, todo['description'].lower())
            elif self.sort_by == 'priority':
                priority_order = {'high': 0, 'medium': 1, 'low': 2}
                return (completed, priority_order[todo.get('priority', 'medium')])
            else:  # created
                return (completed, todo['created_at'])
        
        self.todos.sort(key=get_sort_key, reverse=self.sort_reverse)
    


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
        self.undo_manager = UndoManager()

    def save_state(self):
        """Save current state for undo/redo"""
        state = {
            'projects': [{
                'name': p.name,
                'todos': copy.deepcopy(p.todos),
                'sort_by': p.sort_by,
                'sort_reverse': p.sort_reverse,
                'categories': list(p.categories)
            } for p in self.projects],
            'project_selection': self.project_selection,
            'todo_selection': self.todo_selection,
            'show_completed': self.show_completed
        }
        self.undo_manager.push_state(state)

    def restore_state(self, state):
        """Restore from a saved state"""
        if not state:
            return False
            
        self.projects = []
        for p in state['projects']:
            project = Project(p['name'])
            project.todos = p['todos']
            project.sort_by = p['sort_by']
            project.sort_reverse = p['sort_reverse']
            project.categories = set(p['categories'])
            self.projects.append(project)
            
        self.project_selection = state['project_selection']
        self.todo_selection = state['todo_selection']
        self.show_completed = state['show_completed']
        return True

    def add_todo(self, description: str, due_date: Optional[str] = None, 
                priority: str = 'medium', categories: List[str] = None) -> None:
        self.save_state()  # Save state before modification
        categories = categories or []
        
        todo = {
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'due_date': due_date,
            'priority': priority,
            'categories': categories
        }
        self.projects[self.project_selection].todos.append(todo)
        self.projects[self.project_selection].sort_todos()
        self.save_data()

    def search_todos(self, query: str):
        """Search todos across all projects"""
        results = []
        query = query.lower()
        for project in self.projects:
            for todo in project.todos:
                # Add completion status check
                if (query in todo['description'].lower() or
                    any(query in cat.lower() for cat in todo.get('categories', [])) or
                    query in todo.get('priority', '').lower() or
                    (query == 'completed' and todo['completed']) or
                    (query == 'pending' and not todo['completed'])):
                    results.append((project.name, todo))
        return results

    def cycle_priority(self):
        if not self.projects or not self.projects[self.project_selection].todos:
            return
            
        todo = self.projects[self.project_selection].todos[self.todo_selection]
        priorities = ['low', 'medium', 'high']
        current_priority = todo.get('priority', 'medium')
        
        # Find current index and get next priority
        current_index = priorities.index(current_priority)
        next_index = (current_index + 1) % len(priorities)
        todo['priority'] = priorities[next_index]
        
        self.projects[self.project_selection].sort_todos()
        self.save_data()
        
    def toggle_todo(self):
        self.save_state()  # Save state before modification
        if not self.projects or not self.projects[self.project_selection].todos:
            return
        todos = self.projects[self.project_selection].todos
        todos[self.todo_selection]['completed'] = not todos[self.todo_selection]['completed']
        self.projects[self.project_selection].sort_todos()  # Sort after toggling
        self.save_data()

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

    def delete_todo(self):
        self.save_state()  # Save state before modification
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

    def edit_todo(self, new_description=None, new_due_date=None, new_priority=None):
        self.save_state()  # Save state before modification
        if not self.projects or not self.projects[self.project_selection].todos:
            return
        todo = self.projects[self.project_selection].todos[self.todo_selection]
        if new_description:
            todo['description'] = new_description
        if new_due_date is not None:
            todo['due_date'] = new_due_date if new_due_date else None
        if new_priority:
            todo['priority'] = new_priority
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
    # Priority indicators
    priority_indicators = {
        'high': '*** ',
        'medium': '** ',
        'low': '* ',
    }
    
    prefix = "✓ " if todo['completed'] else "☐ "
    priority = todo.get('priority', 'medium')
    priority_prefix = priority_indicators[priority] if not todo['completed'] else ""
    
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
    
    return f"{prefix}{priority_prefix}{todo['description']}{due_date_str}"

def draw_status_bar(stdscr, todo_manager):
    """Draw status bar at bottom of screen with current context"""
    height, width = stdscr.getmaxyx()
    
    # Get current project info
    active_project = (todo_manager.projects[todo_manager.project_selection].name 
                     if todo_manager.projects else "No Project")
    
    # Get todo stats
    if todo_manager.projects:
        todos = todo_manager.projects[todo_manager.project_selection].todos
        total = len(todos)
        completed = len([t for t in todos if t['completed']])
        uncompleted = total - completed
        progress = f"{completed}/{total} (Done: {completed}, Todo: {uncompleted})"
    else:
        progress = "0/0 (Done: 0, Todo: 0)"

    # Build status message
    status = (f" Mode: {todo_manager.active_window.title()} | "
             f"Project: {active_project} | "
             f"Tasks: {progress} | "
             f"Theme: {todo_manager.theme_manager.current_theme} ")
    
    # Pad with spaces to fill the width
    status = status + " " * (width - len(status) - 1)
    
    # Draw the status bar with reverse colors for visibility
    try:
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(height-1, 0, status)
        stdscr.attroff(curses.A_REVERSE)
    except curses.error:
        pass  # Ignore if status bar doesn't fit

def show_help_window(stdscr, todo_manager):
    """Display help window with keyboard shortcuts"""
    max_y, max_x = stdscr.getmaxyx()
    
    # Calculate window dimensions with bounds checking
    height = min(30, max_y - 4)
    width = min(70, max_x - 4)
    start_y = (max_y - height) // 2
    start_x = (max_x - width) // 2
    
    # Create a shadow window first with dark grey color
    shadow_win = curses.newwin(height, width, start_y + 1, start_x + 1)
    
    # Initialize dark grey color if not already defined
    try:
        curses.init_color(16, 200, 200, 200)  # Dark grey (RGB values: 0-1000)
        curses.init_pair(20, 16, 16)  # Create a new color pair for shadow
        shadow_win.bkgd(' ', curses.color_pair(20))
    except curses.error:
        # Fallback to dim attribute if custom color fails
        shadow_win.bkgd(' ', curses.A_DIM)
    
    shadow_win.refresh()
    
    # Create main help window on top of shadow
    help_win = curses.newwin(height, width, start_y, start_x)
    help_win.bkgd(' ', curses.color_pair(6))
    
    # Fill entire window with background (safely)
    for y in range(height):
        try:
            help_win.addstr(y, 0, " " * (width - 1), curses.color_pair(6))
        except curses.error:
            pass
    
    help_win.box()
    
    # Draw help window
    help_text = [
        "Keyboard Shortcuts",
        "─" * (width - 3),
        "",
        "Navigation",
        " TAB      - Switch between Projects/Todos",
        " ↑/↓      - Move selection up/down",
        "",
        "Other Actions",
        " a        - Add project/todo",
        " d        - Delete project/todo",
        " e        - Edit todo",
        " SPACE    - Toggle completion",
        " p        - Cycle priority",
        " s        - Sort todos",
        " h        - Hide/show completed",
        " /        - Search todos",
        "",
        "Other",
        " t        - Change theme",
        " u        - Undo",
        " Ctrl+r   - Redo",
        " r        - Restore backup",
        " ?        - Show this help",
        " q        - Quit"
    ]
    
    try:
        for i, line in enumerate(help_text):
            if i >= height - 3:
                break
            
            # Clear the line safely
            help_win.addstr(i + 1, 1, " " * (width - 2), curses.color_pair(6))
            
            if i == 0:  # Title
                pos_x = max(2, (width - len(line)) // 2)
                help_win.attron(curses.A_BOLD | curses.color_pair(4))
                help_win.addstr(i + 1, pos_x, line[:width-4])
                help_win.attroff(curses.A_BOLD | curses.color_pair(4))
            elif i == 1:  # Separator
                help_win.addstr(i + 1, 2, line[:width-4], curses.color_pair(4))
            elif line.strip() and not line.startswith(' '):  # Section headers
                help_win.attron(curses.color_pair(4))
                help_win.addstr(i + 1, 2, line[:width-4])
                help_win.attroff(curses.color_pair(4))
            else:  # Regular lines
                help_win.addstr(i + 1, 2, line[:width-4])
        
        # Footer
        if height > 4:
            footer = "Press any key to close"
            footer_x = max(2, (width - len(footer)) // 2)
            help_win.addstr(height-2, 1, " " * (width - 2), curses.color_pair(6))
            help_win.addstr(height-2, footer_x, footer[:width-4], curses.color_pair(8))
        
        help_win.refresh()
        shadow_win.refresh()
        help_win.getch()
        
        # Clean up
        help_win.clear()
        help_win.refresh()
        shadow_win.clear()
        shadow_win.refresh()
        
    except curses.error:
        pass

def main(stdscr):
    curses.start_color()
    curses.curs_set(0)
    
    todo = TodoManager()
    todo.theme_manager.init_nord_theme()
    
    max_y, max_x = stdscr.getmaxyx()
    
    project_win = curses.newwin(max_y-4, max_x//3, 3, 0)
    todo_win = curses.newwin(max_y-4, (2*max_x//3)-1, 3, max_x//3+1)
    
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
        commands = (" [?] Help | [TAB] Switch window | [a] + | [d] - | [e] Edit | "
                   "[space] Toggle | [p] Priority | [s] Sort | [h] Hide/Show | [q] Quit")
        stdscr.addstr(2, 0, commands)

        # Draw project window
        project_win.addstr(0, 2, "Projects")
        for i, project in enumerate(todo.projects):
            style = curses.A_REVERSE if i == todo.project_selection and todo.active_window == 'projects' else curses.A_NORMAL
            project_win.addstr(i+1, 2, f"• {project.name}", style)

        # Draw todo window with safe header rendering
        if not todo.projects:
            todo_win.addstr(0, 2, "Todos - No Project")
        else:
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
                try:
                    todo_win.addstr(i+1, 2, display_str, style)
                except curses.error:
                    # Handle case where todo text is too long for window
                    pass

        stdscr.refresh()
        project_win.refresh()
        todo_win.refresh()
        
        draw_status_bar(stdscr, todo)
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
                    
                    stdscr.clear()
                    stdscr.addstr(max_y-2, 0, "Set priority (h)igh, (m)edium, (l)ow: ")
                    stdscr.clrtoeol()
                    priority_key = stdscr.getch()
                    
                    priority = 'medium'  # Default
                    if priority_key == ord('h'):
                        priority = 'high'
                    elif priority_key == ord('l'):
                        priority = 'low'
                    
                    if description:
                        due_date = parse_due_date(due_date_str) if due_date_str else None
                        todo.add_todo(description, due_date, priority)
            
            curses.noecho()
            curses.curs_set(0)
        elif key == ord('d'):
            if todo.active_window == 'projects':
                todo.delete_project(stdscr)
            else:
                todo.delete_todo()
        elif key == ord('p') and todo.active_window == 'todos':
                todo.cycle_priority()
        elif key == ord(' '):
            if todo.active_window == 'todos':
                todo.toggle_todo()
        elif key == ord('?'):
            show_help_window(stdscr, todo)
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
                
                stdscr.clear()
                stdscr.addstr(max_y-2, 0, "Edit priority (h)igh, (m)edium, (l)ow, or leave empty to keep current: ")
                stdscr.clrtoeol()
                priority_key = stdscr.getch()
                
                new_priority = None
                if priority_key == ord('h'):
                    new_priority = 'high'
                elif priority_key == ord('m'):
                    new_priority = 'medium'
                elif priority_key == ord('l'):
                    new_priority = 'low'
                
                if new_desc or new_date_str or new_priority:
                    new_date = parse_due_date(new_date_str) if new_date_str else current_todo.get('due_date')
                    todo.edit_todo(
                        new_description=new_desc if new_desc else current_todo['description'],
                        new_due_date=new_date,
                        new_priority=new_priority
                    )
                
                curses.noecho()
                curses.curs_set(0)
        elif key == ord('s') and todo.active_window == 'todos':
            stdscr.addstr(max_y-2, 0, "Sort by (n)ame, (d)ue date, or (p)riority?: ")
            stdscr.clrtoeol()
            sort_key = stdscr.getch()
            if sort_key == ord('n'):
                todo.toggle_sort('description')
            elif sort_key == ord('d'):
                todo.toggle_sort('due_date')
            elif sort_key == ord('p'):
                todo.toggle_sort('priority')   
        elif key == ord('/'):  # Add search functionality
            curses.echo()
            curses.curs_set(1)
            max_y, max_x = stdscr.getmaxyx()
            stdscr.addstr(max_y-2, 0, "Search: ")
            stdscr.clrtoeol()
            query = stdscr.getstr().decode('utf-8')
            
            if query:
                results = todo.search_todos(query)
                if results:
                    # Create search results window
                    search_win = curses.newwin(max_y-3, max_x-2, 3, 1)
                    search_win.box()
                    search_win.addstr(0, 2, f"Search Results for '{query}'")
                    
                    for i, (project_name, task) in enumerate(results, 1):
                        if i >= max_y-5:  # Prevent overflow
                            break
                        display_str = f"{project_name}: {format_todo_display(task)}"
                        search_win.addstr(i, 2, display_str, get_todo_style(task))
                    
                    search_win.refresh()
                    search_win.getch()
            
            curses.noecho()
            curses.curs_set(0)
        elif key == ord('t'):
            todo.theme_manager.toggle_theme()
        elif key == ord('u'):  # Undo
            current_state = {
                'projects': [{
                    'name': p.name,
                    'todos': copy.deepcopy(p.todos),
                    'sort_by': p.sort_by,
                    'sort_reverse': p.sort_reverse,
                    'categories': list(p.categories)
                } for p in todo.projects],
                'project_selection': todo.project_selection,
                'todo_selection': todo.todo_selection,
                'show_completed': todo.show_completed
            }
            if todo.restore_state(todo.undo_manager.undo(current_state)):
                todo.save_data()
                
        elif key == 18:  # Ctrl+R for Redo
            current_state = {
                'projects': [{
                    'name': p.name,
                    'todos': copy.deepcopy(p.todos),
                    'sort_by': p.sort_by,
                    'sort_reverse': p.sort_reverse,
                    'categories': list(p.categories)
                } for p in todo.projects],
                'project_selection': todo.project_selection,
                'todo_selection': todo.todo_selection,
                'show_completed': todo.show_completed
            }
            if todo.restore_state(todo.undo_manager.redo(current_state)):
                todo.save_data()
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
        elif key == ord('?'):
            show_help_window(stdscr, todo)

if __name__ == "__main__":
    curses.wrapper(main)
