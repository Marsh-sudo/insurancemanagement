from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from customer import models as CMODEL
from insurance import models  # Replace 'your_app_name' with the actual name of your Django app

class AdminQuestionViewTests(TestCase):
    def test_admin_question_view(self):

        self.user = User.objects.create_user(username='testadmin', password='testpassword')

        # Create a customer for testing
        self.customer = CMODEL.Customer.objects.create(user=self.user)
        # Create sample questions for testing
        question1 = models.Question.objects.create(customer=self.customer,description='Question 1')
        question2 = models.Question.objects.create(customer=self.customer,description='Question 2')

        # Create a client and submit a GET request to the admin question view
        client = Client()
        response = client.get(reverse('admin-question'))

        # Assertions based on the expected behavior of your function
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'insurance/admin_question.html')  # Check for the correct template used
        self.assertQuerysetEqual(response.context['questions'], [repr(question1), repr(question2)], ordered=False)

class UpdateQuestionViewTests(TestCase):
    def test_update_question_view_form_submission(self):

        self.user = User.objects.create_user(username='testadmin', password='testpassword')

        # Create a customer for testing
        self.customer = CMODEL.Customer.objects.create(user=self.user)

        # Create a sample question for testing
        question = models.Question.objects.create(customer=self.customer,description='Sample Question',admin_comment="nothing")

        # Create a client and log in the user
        client = Client()

        # Create a dictionary with valid form data
        form_data = {
            'description': 'Updated Question Text',
            'admin_comment': 'Admin Comment',
            # Add other fields as needed
        }

        # Submit a POST request with the form data to the update question view
        response = client.post(reverse('update-question', args=[question.id]), data=form_data)

        # Assertions based on the expected behavior of your function
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect status
        self.assertRedirects(response, reverse('admin-question'))

        # Check if the question information is updated in the database
        question.refresh_from_db()
        self.assertEqual(question.description, 'Updated Question Text')
        self.assertEqual(question.admin_comment, 'Admin Comment')

    # def test_update_question_view_invalid_form_submission(self):
    #     # Create a sample question for testing
    #     question = models.Question.objects.create(customer=self.customer,description='Sample Question')

    #     # Create a client and submit a POST request without any form data to trigger form validation errors
    #     client = Client()
    #     response = client.post(reverse('update-question', args=[question.id]))

    #     # Assertions based on the expected behavior of your function
    #     self.assertEqual(response.status_code, 200)  # Check for a successful response
    #     self.assertContains(response, 'This field is required.')  # Check for form validation errors

    #     # Check if the question information is not updated in the database
    #     question.refresh_from_db()
    #     self.assertEqual(question.description, 'Sample Question')
