import attr

from bluearchive.models.enums import Role, CharacterType, School, Position, Weapon, DamageType, ArmorType


@attr.s
class BuruakaQuery:
    """
    Query object to specify which student to get.
    """
    role: Role | None = attr.field(default=None)
    type: CharacterType | None = attr.field(default=None)
    school: School | None = attr.field(default=None)
    position: Position | None = attr.field(default=None)
    weapon: Weapon | None = attr.field(default=None)
    damage: DamageType | None = attr.field(default=None)
    armor: ArmorType | None = attr.field(default=None)

    def Role(self, role: Role) -> "BuruakaQuery":
        """Set 'Role' field of query.

        Args:
            role (Role): certain role to query with.

        Returns:
            BuruakaQuery: returns BuruakaQuery object itself for method chaining.
        """
        self.role = role
        return self

    def Type(self, type: CharacterType) -> "BuruakaQuery":
        """Set 'Type' field of query.

        Args:
            type (CharacterType): certain type to query with.

        Returns:
            BuruakaQuery: returns BuruakaQuery object itself for method chaining.
        """
        self.type = type
        return self

    def School(self, school: School) -> "BuruakaQuery":
        """Set 'School' field of query.

        Args:
            school (School): certain school to query with.

        Returns:
            BuruakaQuery: returns BuruakaQuery object itself for method chaining.
        """
        self.school = school
        return self

    def Position(self, position: Position) -> "BuruakaQuery":
        """Set 'Position' field of query.

        Args:
            position (Position): certain position to query with.

        Returns:
            BuruakaQuery: returns BuruakaQuery object itself for method chaining.
        """
        self.position = position
        return self

    def Weapon(self, weapon: Weapon) -> "BuruakaQuery":
        """Set 'Weapon' field of query.

        Args:
            weapon (Weapon): certain weapon to query with.

        Returns:
            BuruakaQuery: returns BuruakaQuery object itself for method chaining.
        """
        self.weapon = weapon
        return self

    def Damage(self, damage: DamageType) -> "BuruakaQuery":
        """Set 'Damage' field of query.

        Args:
            damage (Damage): certain damage to query with.

        Returns:
            BuruakaQuery: returns BuruakaQuery object itself for method chaining.
        """
        self.damage = damage
        return self

    def Armor(self, armor: ArmorType) -> "BuruakaQuery":
        """Set 'Armor' field of query.

        Args:
            armor (Armor): certain armor to query with.

        Returns:
            BuruakaQuery: returns BuruakaQuery object itself for method chaining.
        """
        self.armor = armor
        return self

    def build(self) -> str:
        """Build query parameters.

        Returns:
            str: query parameters as string.
        """
        queries: list[str] = []
        if self.role is not None:
            queries.append(f"role={self.role.value}")
        if self.type is not None:
            queries.append(f"type={self.type.value}")
        if self.school is not None:
            queries.append(f"school={self.school.value}")
        if self.position is not None:
            queries.append(f"position={self.position.value}")
        if self.weapon is not None:
            queries.append(f"weapon={self.weapon.value}")
        if self.damage is not None:
            queries.append(f"damage={self.damage.value}")
        if self.armor is not None:
            queries.append(f"armor={self.armor.value.replace(' ', '%20')}")
        return "/query?" + "&".join(queries)
