"""
Copyright 2020 ООО «Верме»
"""

from django.db import models


class OrganizationQuerySet(models.QuerySet):

    def tree_downwards(self, root_org_id):
        """
        Возвращает корневую организацию с запрашиваемым root_org_id и всех её детей любого уровня вложенности
        :type root_org_id: int
        """

        all_organizations = self.all().order_by('id')
        child_id_list = {root_org_id, }

        for org in all_organizations:
            if org.parent_id in child_id_list:
                child_id_list.add(org.id)
        del all_organizations

        return self.filter(id__in=child_id_list)

    def tree_upwards(self, child_org_id):
        """
        Возвращает корневую организацию с запрашиваемым child_org_id и всех её родителей любого уровня вложенности
        :type child_org_id: int
        """

        all_organizations = self.all().order_by('-id')
        parent_id_list = {child_org_id, }

        for org in all_organizations:
            if org.id in parent_id_list:
                parent_id_list.add(org.parent_id)
        del all_organizations

        return self.filter(id__in=parent_id_list)


class Organization(models.Model):
    """ Организаци """

    objects = OrganizationQuerySet.as_manager()

    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name="Название")
    code = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name="Код")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Вышестоящая организация",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Организация"
        verbose_name = "Организации"

    def __str__(self):
        return self.name

    def parents(self):
        """
        Возвращает всех родителей любого уровня вложенности
        :rtype: django.db.models.QuerySet
        """
        return type(self).objects.tree_upwards(self.id).exclude(id=self.id)

    def childrens(self):
        """
        Возвращает всех детей любого уровня вложенности
        :rtype: django.db.models.QuerySet
        """
        return type(self).objects.tree_downwards(self.id).exclude(id=self.id)
