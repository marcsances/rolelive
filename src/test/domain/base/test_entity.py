from test.domain.base.mocks_entity import EmptyEntity, EmptyEntityWithMethods, EntityWithOneField, EntityWithList, \
    EntityWithChild, EntityWithMoreChild, EntityWithDict


class TestEntity:

    def test_to_json_given_empty_dict_returns_empty_dict(self):
        empty_entity = EmptyEntity()
        assert empty_entity.to_dict() == {}

    def test_to_json_given_entity_with_methods_returns_empty_json(self):
        empty_entity_with_methods = EmptyEntityWithMethods()
        assert empty_entity_with_methods.to_dict() == {}

    def test_to_json_given_entity_with_single_field_returns_field(self):
        entity_with_field = EntityWithOneField()
        assert entity_with_field.to_dict() == {"my_field": "Hello"}

    def test_to_json_given_entity_with_list_returns_list(self):
        entity_with_list = EntityWithList()
        assert entity_with_list.to_dict() == {"my_list": ["item1", "item2"]}

    def test_to_json_given_entity_with_child_returns_all_fields(self):
        entity_with_children = EntityWithChild()
        assert entity_with_children.to_dict() == {"my_field": "Hey there", "my_child": {"my_field": "Hello"}}

    def test_to_json_given_entity_with_multilevel_child_returns_all_fields(self):
        entity_with_more_children = EntityWithMoreChild()
        assert entity_with_more_children.to_dict() == \
               {
                   "my_field": "Deeper",
                   "my_child": {
                       "my_field": "Hey there",
                       "my_child": {"my_field": "Hello"}
                   }, "another_child": {
                   "my_list": ["item1", "item2"]
               }, "this_one_is_empty": {}
               }

    def test_to_json_given_entity_with_dict_returns_dict(self):
        entity_with_dict = EntityWithDict()
        assert entity_with_dict.to_dict() == {
            "my_dict": {
                "key": "value",
                "foo": "bar"
            }
        }

    def test_from_json_empty_entity(self):
        empty_entity = EmptyEntity().from_dict({"this_field": "won't exist"})
        assert empty_entity.__dict__ == {}

    def test_from_json_entity_with_list(self):
        entity_with_list = EntityWithList().from_dict({"my_list": ["new list!", "with items!"], "this_field": "won't "
                                                                                                              "exist"})
        assert entity_with_list.my_list == ["new list!", "with items!"]
        assert "this_field" not in entity_with_list.__dict__

    def test_from_json_entity_with_child(self):
        entity_with_child = EntityWithChild().from_dict({"my_field": "Nice", "my_child": {"my_field": "One"}})
        assert entity_with_child.my_field == "Nice"
        assert entity_with_child.my_child.my_field == "One"

    def test_from_json_entity_with_more_child_and_default_values_are_applied(self):
        entity_with_more_child = EntityWithMoreChild().from_dict(
            {"my_field": "Something", "this_one_is_empty": {"and_it_will": "still_be"}})
        assert entity_with_more_child.my_field == "Something"
        assert entity_with_more_child.my_child.my_field == "Hey there"
        assert entity_with_more_child.another_child.my_list == ["item1", "item2"]
        assert entity_with_more_child.this_one_is_empty.__dict__ == {}

    def test_from_json_entity_with_dict_dict_is_restored(self):
        entity_with_dict = EntityWithDict().from_dict({"my_dict": {"new": "dictionary"}})
        assert entity_with_dict.my_dict["new"] == "dictionary"
