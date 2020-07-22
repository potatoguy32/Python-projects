from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def add_task(task, deadline):
    addition = Table(task=task, deadline=deadline)
    session.add(addition)
    session.commit()


def today_tasks():
    query = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    print(f'Today {datetime.today().strftime("%d %b")}:')
    if len(query) == 0:
        print('Nothing to do!')
    else:
        for index, element in enumerate(query, start=1):
            print(f'{index}. {element}')
    print('')


def show_tasks():
    query = session.query(Table).order_by(Table.deadline).all()
    if len(query) > 0:
        for index, row in enumerate(query, start=1):
            print(f"{index}. {row}. {row.deadline.strftime('%d %b')}")
    else:
        print('Nothing to do!')
    print("")


def drop_task(number):
    query = session.query(Table).order_by(Table.deadline).all()
    session.delete(query[number - 1])
    session.commit()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

choice = ""
while choice != 0:
    choice = int(input("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit \n"""))

    if choice == 1:
        today_tasks()

    if choice == 2:
        for i in range(7):
            day = datetime.today() + timedelta(days=i)
            query = session.query(Table).filter(Table.deadline == day.date()).all()
            print(f"{day.strftime('%A %d %b')}:")
            if len(query) > 0:
                for index, row in enumerate(query, start=1):
                    print(f"{index}. {row}")
                print("")
            else:
                print('Nothing to do!\n')

    if choice == 3:
        print('All tasks:')
        show_tasks()

    if choice == 4:
        query = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print('Missed tasks')
        if len(query) > 0:
            for index, row in enumerate(query, start=1):
                print(f'{index}. {row}. {row.deadline.strftime("%A %b")}')
            print("")
        else:
            print("Nothing is missed!\n")

    if choice == 5:
        new_task = input('Enter task\n')
        new_deadline = datetime.strptime(input('Enter deadline\n'), '%Y-%m-%d')
        add_task(new_task, new_deadline)
        print('The task has been added!\n')

    if choice == 6:
        print('Chose the number of the task you want to delete:')
        show_tasks()
        selection = int(input())
        drop_task(selection)
        print('The task has been deleted\n')

    if choice == 0:
        print('\nBye!')
