'''Program to keep track of working hours per project, including design and other phases that aren't tracked by Wakatime'''

import json
import inquirer
import logging as log


class WorkHours:

    def __init__(self, filename, encoder, decoder):
        self.filename = filename
        self.encoder = encoder
        self.decoder = decoder
        self.projects = {}
        self.quit_option = 'quit'
        self.return_option = 'return'

    def choicify_choices_with_return(self, choices):
        choices.append(self.return_option)
        choices = [choice.title() for choice in choices]
        return choices

    def choicify_choices_with_quit(self, choices):
        choices.append(self.quit_option)
        choices = [choice.title() for choice in choices]
        return choices

    def compare_with_quit_or_return(self, value):
        return value == self.quit_option or value == self.return_option

    def open_file_or_create(self):
        try:
            file = open(self.filename)
        except FileNotFoundError:
            data = '{}'
            print('File not found, creating new file\n')
            file = open(self.filename, 'w')
            file.write(data)
            file.close()
            return data
        else:
            data = file.read()
            file.close()
            return data

    def __str__(self):
        print(f'__str__: {self.projects}')

    def save_workhours(self):
        data = json.dumps(self.projects, cls=self.encoder, indent=4)
        file = open(self.filename, 'w')
        file.write(data)
        file.close()
        return

    def load_workhours(self):
        data = self.open_file_or_create()
        self.projects = json.loads(data, object_hook=self.decoder)

    def get_project(self, message):
        question = {
            inquirer.List(
                'project',
                message=message,
                choices=self.choicify_choices_with_return(
                    list(self.projects.keys()))
            )
        }
        response = inquirer.prompt(question)
        project_name = None
        project = None
        if not self.compare_with_quit_or_return(response['project'].lower()):
            project = self.projects.get(response['project'].lower())
            if project is not None:
                project_name = response['project'].lower()
        return project_name, project

    def get_stage(self, project, message):
        question = {
            inquirer.List(
                'stage',
                message=message,
                choices=self.choicify_choices_with_return(
                    list(project.keys()))
            )
        }
        response = inquirer.prompt(question)
        stage_name = None
        if not self.compare_with_quit_or_return(response['stage'].lower()):
            stage = project.get(response['stage'].lower())
            if stage is not None:
                stage_name = response['stage'].lower()
        return stage_name

    def add_project(self):
        question = {
            inquirer.Text(
                'name', message="What's the name of the new project? Or type \"quit\" to quit")
        }
        response = inquirer.prompt(question)
        if not self.compare_with_quit_or_return(response['name'].lower()):
            if self.projects.get(response['name'].lower()) is not None:
                print(
                    f'Project: {response["name"].title()} already exists.\n')
            else:
                self.projects[response['name'].lower()] = {}
                print(f'Project: {response["name"].title()} added.\n')

    def add_stage(self):
        message = 'Which project would you like to add a stage to? Or enter \"quit\" to quit'
        project_name, project = self.get_project(message)
        if project_name is not None:
            question = {
                inquirer.Text(
                    'name', message="What's the name of the new stage? Or type \"quit\" to quit"
                )
            }
            response = inquirer.prompt(question)
            stage_name = response['name'].lower()
            if stage_name != self.quit_option:
                stage = project.get(stage_name)
                if stage is not None:
                    print(
                        f'Stage: \"{response["name"].title()}\" already exists in project: \"{project_name.title()}\".\n')
                else:
                    valid_input = False
                    question = {
                        inquirer.Text(
                            name='price',
                            message='What is the price per hour? Or enter \"quit\" to quit'
                        )
                    }
                    while not valid_input:
                        response = inquirer.prompt(question)
                        response = response['price']
                        if response == self.quit_option:
                            break
                        else:
                            try:
                                response = float(response)
                            except ValueError:
                                print('Please enter a valid number\n')
                            else:
                                if response < 0:
                                    print('Please enter a positive number\n')
                                    continue
                                else:
                                    if response % 1 == 0:
                                        response = int(response)
                                    valid_input = True
                                    project[stage_name] = {
                                        'hours': 0,
                                        'price': response
                                    }
                                    print(
                                        f'Stage: \"{stage_name.title()}\" added in project {project_name.title()}.\n'
                                    )

    def add_hours(self):
        message = 'Which project would you like to add hours to?'
        project_name, project = self.get_project(message)
        if project_name is not None:
            message = 'Which stage would you like to add hours to?'
            stage_name = self.get_stage(project, message)
            if stage_name is not None:
                valid_input = False
                hours = None
                question = {
                    inquirer.Text(
                        'number', message='How many hours would you like to add? Or enter \"quit\" to quit')
                }
                while not valid_input:
                    hours = inquirer.prompt(question)
                    response = hours['number']
                    if response == self.quit_option:
                        break
                    else:
                        try:
                            response = float(response)
                        except ValueError:
                            print('Please enter a valid number\n')
                        else:
                            if response < 0:
                                print('Please enter a positive number\n')
                                continue
                            else:
                                if response % 1 == 0:
                                    response = int(response)
                                valid_input = True
                                project[stage_name]["hours"] += response
                                print(
                                    f'{response} hours added to stage: {stage_name.title()} of project: {project_name.title()}'
                                )

    def add(self):
        project = 'add project'
        stage = 'add stage'
        hours = 'add hours'
        list_of_choices = self.choicify_choices_with_return(
            [project, stage, hours])
        choice = {
            inquirer.List(
                'add', message=f'What would you like to add?',
                choices=list_of_choices
            )
        }
        response = inquirer.prompt(choice)
        match_value = response['add'].lower()
        match match_value:
            case 'add project':
                self.add_project()
            case 'add stage':
                self.add_stage()
            case 'add hours':
                self.add_hours()

    def consult_project(self):
        message = 'Which project would you like to consult?'
        project_name, project = self.get_project(message)
        if project_name is not None:
            print(f'Project: {project_name.title()}\n')
            stage_index = 1
            total_hours = 0
            total_price = 0
            for stage, dct in project.items():
                print(
                    f'\tStage {stage_index}: {stage.title()} --- {dct["hours"]} hours --- €{dct["price"]} per hour')
                stage_index += 1
                total_hours += dct["hours"]
                total_price += dct["hours"] * dct["price"]
            print(
                f'\n- Total hours: {total_hours}\n- Total price: €{total_price}\n')

    def consult_stage(self):
        message = 'For which project would you like to consult a stage?'
        project_name, project = self.get_project(message)
        if project_name is not None:
            message = 'Which stage would you like to consult?'
            stage_name = self.get_stage(project, message)
            if stage_name is not None:
                print(f'Project: {project_name.title()}\n')
                stage_index = list(project.keys()).index(stage_name) + 1
                print(
                    f'\tStage {stage_index}: {stage_name.title()} --- {project[stage_name]["hours"]} hours --- €{project[stage_name]["price"]} per hour\n'
                )
            print(
                f'- Total price: €{project[stage_name]["hours"] * project[stage_name]["price"]}\n')

    def get_stages(self, project, message):
        question = {
            inquirer.Checkbox(
                name="stages",
                message=message,
                choices=[key.title() for key in list(project.keys())]
            )
        }
        response = inquirer.prompt(question)
        response = [stage.lower() for stage in response['stages']]
        return response

    def consult_stages(self):
        message = 'For which project would you like to consult stages?'
        project_name, project = self.get_project(message)
        if project_name is not None:
            message = 'Which stages would you like to consult?'
            stages = self.get_stages(project, message)
            print(f'Project: {project_name.title()}\n')
            total_hours = 0
            total_price = 0
            list_of_stages = list(project.keys())
            for stage in stages:
                print(
                    f'\tStage  {list_of_stages.index(stage) + 1}: {stage.title()} --- {project[stage]["hours"]} hours --- €{project[stage]["price"]} per hour')
                total_hours += project[stage]["hours"]
                total_price += project[stage]["hours"] * \
                    project[stage]['price']
            print(
                f'\n- Total hours: {total_hours}\n- Total price: €{total_price}\n')

    def consult(self):
        project = 'consult project'
        stage = 'consult stages'
        hours = 'consult stage'
        list_of_choices = self.choicify_choices_with_return(
            [project, stage, hours]
        )
        choice = {
            inquirer.List(
                'consult', message=f'What would you like to consult?',
                choices=list_of_choices
            )
        }
        response = inquirer.prompt(choice)
        match_value = response['consult'].lower()
        match match_value:
            case 'consult project':
                self.consult_project()
            case 'consult stages':
                self.consult_stages()
            case 'consult stage':
                self.consult_stage()

    def edit(self):
        pass
        # TODO: Implement edit function to edit project name, stage name, hours or price

    def delete(self):
        pass
        # TODO: Implement delete function to delete project, stage or reset hours to 0 or reset price to 0

    def print_predefined_stages(self):
        print("""\nThe Software development stages are:
        Stage 1: Plan and brainstorm.
        Stage 2: Analyze requirements.
        Stage 3: Design the mockups.
        Stage 4: Develop the code.
        Stage 5: Test the product.
        Stage 6: Deploy the product.
        Stage 7: Maintenance & support.\n""")

    def run(self):
        exit = False
        print('Welcome to the workhours program.\n')
        list_of_choices = [
            'add project, stage or hours',
            'consult project, stages or stage',
            # 'edit project, stage or hours',
            # 'delete project, stage or hours',
            'print predefined stages'
        ]
        list_of_choices = self.choicify_choices_with_quit(list_of_choices)
        choice = {
            inquirer.List(
                'menu', message=f'What would you like to do?',
                choices=list_of_choices)
        }
        while not exit:
            response = inquirer.prompt(choice)
            response = response['menu'].lower()
            match response:  # Quit program
                case self.quit_option:
                    exit = True
                    print('Saving workhours.\n')
                    self.save_workhours()
                    print('Workhours saved.\n')
                    print('Quitting program.\n')
                case 'add project, stage or hours':  # Add project, stage or hours
                    log.info('Add project, stage or hours')
                    self.add()
                case 'consult project, stages or stage':  # Consult project, stage or hours
                    self.consult()
                case 'edit project name, stage name or hours':  # Edit project, stage or hours
                    self.edit()
                case 'delete project, stage or reset hours':  # Delete project, stage or hours
                    self.delete()
                case 'print predefined stages':
                    self.print_predefined_stages()
