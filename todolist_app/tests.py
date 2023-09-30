from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import TodoTask

class TodoTaskAPITest(TestCase):

    def setup_forupdate(self):
        self.client = APIClient()
        self.task = TodoTask.objects.create(user=self.user, name='Test Task', description='Test Description',deadline='2023-10-01T12:00:00Z')


    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    #REGISTER function tests

    def test_user_register(self):
        # Define your test data for user registration
        datas = [{
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
        },{
            'username': 'newuser1',
            'password': 'newpassword1',
            'email': 'newuser1@example.com',
        }]

        for data in datas:
        
        # sending  a POST request to the 'user_register' view
            response = self.client.post(reverse('todolist_app:user_register'), data)
            
            # Assert the response status code and content
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {'message': 'User registered successfully.'})
            print (response.content)
            
            # checking if the user has been created in the database
            self.assertTrue(User.objects.filter(username='newuser').exists())

        
    def test_user_register_invalid_data(self):
        invalid_data = {
            'username': '',
            'password': '',
            'email': ''
        }

        response = self.client.post(reverse('todolist_app:user_register'), invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    #User Login tests

    def test_user_login(self):
        # Define your test data for user registration
        datas = [{
            'username': 'testuser',
            'password': 'testpassword',
        }]

        for data in datas:
        
        # Sending a POST request to the 'user_register' view
            response = self.client.post(reverse('todolist_app:user_login'), data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print (response.content)
            self.assertEqual(response.data, {'message': 'Login successful.'})
    
    

    def test_user_login_invalid_data(self):
        invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        response = self.client.post(reverse('todolist_app:user_login'), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_user_login_user_not_found(self):
        invalid_data = {
            'username': 'nonexistentuser',
            'password': 'password'
        }

        response = self.client.post(reverse('todolist_app:user_login'), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

                
    #Create todo tasks tests

    def test_create_todo_task(self):
        # Define your test data for user registration
        data = {
            'name': 'Test Task',
            'description': 'Test description',
            'deadline': '2023-12-31T23:59:59Z',  #this should be in correct format of datetime
        }

        response = self.client.post(reverse('todolist_app:create_todo_task'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the task was created in the database
        self.assertEqual(TodoTask.objects.count(), 1)
        todo_task = TodoTask.objects.get()
        self.assertEqual(todo_task.name, 'Test Task')
        self.assertEqual(todo_task.description, 'Test description')
            
    def test_create_todo_task_invalid_data(self):
        data = {
            'task_name': 'Test Task',  
            'description': 'This is a test task.'
        }

        response = self.client.post(reverse('todolist_app:create_todo_task'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TodoTask.objects.count(), 0) 
        print (response.content)

    def test_create_todo_task_unauthenticated(self):
        self.client.logout()  # Checking an unauthenticated request
        data = {
            'task_name': 'Test Task',
            'description': 'This is a test task.'
        }

        response = self.client.post(reverse('todolist_app:create_todo_task'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(TodoTask.objects.count(), 0)
        print(response.content)

#Update tasks test

    def test_update_task_with_valid_data(self):

        self.setup_forupdate()
        self.client.force_authenticate(user=self.user)
        updated_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'deadline': '2023-10-02T12:00:00Z'
        }
        url = reverse('todolist_app:update_todo_task', args=[self.task.id])

        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')

    def test_update_task_with_invalid_data(self):

        self.setup_forupdate()
        self.client.force_authenticate(user=self.user)
        invalid_data = {
            'name': '',  # Invalid name (empty string)
            'deadline': '2023-10-02T12:00:00Z'
        }
        url = reverse('todolist_app:update_todo_task', args=[self.task.id])
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_unauthenticated(self):
        
        self.setup_forupdate()
        updated_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'deadline': '2023-10-02T12:00:00Z'
        }
        url = reverse('todolist_app:update_todo_task', args=[self.task.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task_of_other_user(self):

        self.setup_forupdate()
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        
        self.client.force_authenticate(user=other_user)
        updated_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'deadline': '2023-10-02T12:00:00Z'
        }
        url = reverse('todolist_app:update_todo_task', args=[self.task.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_nonexistent_task(self):

        self.client.force_authenticate(user=self.user)
        updated_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'deadline': '2023-10-02T12:00:00Z'
        }
        url = reverse('todolist_app:update_todo_task', args=[999])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #Delete method testing

    def test_delete_todo_task(self):

        self.setup_forupdate()
        self.client.force_authenticate(user=self.user)
        
        url = reverse('todolist_app:delete_todo_task', args=[self.task.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify that the task was deleted from the database
        self.assertEqual(TodoTask.objects.count(), 0)

    def test_delete_todo_task_unauthenticated(self):

        self.setup_forupdate()
        self.client.logout()  # Simulate an unauthenticated request
        
        url = reverse('todolist_app:delete_todo_task', args=[self.task.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Verify that the task was not deleted from the database
        self.assertEqual(TodoTask.objects.count(), 1)

    def test_delete_task_of_other_user(self):

        self.setup_forupdate()
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        
        self.client.force_authenticate(user=other_user)
        
        url = reverse('todolist_app:delete_todo_task', args=[self.task.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Verify that the task was not deleted from the database
        self.assertEqual(TodoTask.objects.count(), 1)

    def test_delete_nonexistent_task(self):

        self.setup_forupdate()
        self.client.force_authenticate(user=self.user)
        
        url = reverse('todolist_app:delete_todo_task', args=[999])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Verify that the task was not deleted from the database
        self.assertEqual(TodoTask.objects.count(), 1)

    # Add similar test methods for other views like 'user_login', 'create_todo_task', 'update_todo_task', 'delete_todo_task'.

    