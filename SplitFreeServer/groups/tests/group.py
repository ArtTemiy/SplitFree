from groups.models.group import Group, GroupSerializer
from groups.tests.common import GroupTestBase


class GroupAPITests(GroupTestBase):
    group_title = 'My Group'

    def test_get(self):
        response = self.client.get(path=self.path_with_name)
        self.assertResponse(response)
        self.assertDictEqual(
            response.data,
            {
                'id': self.group.pk,
                'name': self.group_name,
                'title': self.group_title,
                'created': response.data['created'],
                'admin': self.author.username,
                'members': [self.user.username,],
            }
        )

    def test_no_id(self):
        response = self.client.get('/group')
        self.assertResponse(response, 400)
        self.assertIsNotNone(response.data)

    def test_no_group(self):
        response = self.client.get('/group?name=2864723456')
        self.assertResponse(response, 404)
        self.assertIsNotNone(response.data)

    def test_create(self):
        name2 = 'group2'
        title2 = 'Title 2'
        response = self.client.post(
            path=f'/group?name={name2}',
            data={
                'title': title2,
            },
            format='json',
        )
        self.assertResponse(response)
        self.assertDictEqual(response.data, {
            'id': Group.objects.get(name=name2).pk,
            'name': name2,
            'title': title2,
            'admin': self.author.username,
            'members': [],
            'created': response.data['created'],
        })

    def test_invalid_name(self):
        title_2 = 'Title 2'
        response = self.client.post(
            path='/group?name=group2$$asd',
            data={
                'title': title_2,
            },
            format='json',
        )
        self.assertResponse(response, status_code=400)

    def test_update(self):
        title_updated = 'Title updated'
        response = self.client.put(
            path=self.path_with_name,
            data={
                'title': title_updated
            },
            format='json'
        )
        self.assertResponse(response)
        response_new = self.client.get(self.path_with_name)
        self.assertResponse(response_new)
        self.assertEqual(response_new.data['title'], title_updated)

    def test_delete(self):
        response = self.client.delete(self.path_with_name)
        self.assertResponse(response)
        self.assertEqual(Group.objects.count(), 0)
