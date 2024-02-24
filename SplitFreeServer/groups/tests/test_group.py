from groups.models.group import Group, GroupSerializer
from groups.tests.test_case_group import GroupTestCaseBase


class GroupAPITestsCase(GroupTestCaseBase):
    group_title = 'My Group'

    def test_get(self):
        response = self.client_admin.get(path=self.path_with_name)
        self.assertResponse(response)
        self.assertDictEqual(
            response.data,
            {
                'name': self.group_name,
                'title': self.group_title,
                'created': response.data['created'],
                'admin': self.user_admin.username,
                'members': [self.user_member.username, ],
            }
        )

    def test_no_id(self):
        response = self.client_admin.get('/group')
        self.assertResponse(response, 400)
        self.assertIsNotNone(response.data)

    def test_no_group(self):
        response = self.client_admin.get('/group?name=2864723456')
        self.assertResponse(response, 404)
        self.assertIsNotNone(response.data)

    def test_forbidden_other_user(self):
        self.assertResponse(
            self.client_other.get(
                path=self.path_with_name
            ),
            status_code=403
        )

    def test_forbidden_no_token(self):
        self.assertResponse(
            self.client.get(
                path=self.path_with_name
            ),
            status_code=401
        )

    def test_create(self):
        name2 = 'group2'
        title2 = 'Title 2'
        response = self.client_admin.post(
            path=f'/group',
            data={
                'name': name2,
                'title': title2,
            },
            format='json',
        )
        self.assertResponse(response)
        self.assertDictEqual(response.data, {
            'name': name2,
            'title': title2,
            'admin': self.user_admin.username,
            'members': [],
            'created': response.data['created'],
        })

    def test_invalid_name(self):
        title_2 = 'Title 2'
        response = self.client_admin.post(
            path='/group',
            data={
                'name': 'group2$$asd',
                'title': title_2,
            },
            format='json',
        )
        self.assertResponse(response, status_code=400)

    def already_exist(self):
        response = self.client_admin.post(
            path='/group',
            data={
                'name': self.group.name,
                'title': 'xxx',
            },
            format='json'
        )
        self.assertResponse(response, status_code=400)

    def test_update(self):
        title_updated = 'Title updated'
        response = self.client_admin.put(
            path=self.path_with_name,
            data={
                'title': title_updated
            },
            format='json'
        )
        self.assertResponse(response)
        response_new = self.client_admin.get(self.path_with_name)
        self.assertResponse(response_new)
        self.assertEqual(response_new.data['title'], title_updated)

    def test_delete(self):
        response = self.client_admin.delete(self.path_with_name)
        self.assertResponse(response)
        self.assertEqual(Group.objects.count(), 0)
