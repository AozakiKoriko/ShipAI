class Container:
    def __init__(self, position, weight, description):
        self.position = position
        self.weight = weight
        self.description = description

    def is_valid(self):
        if self.description in ['NAN', 'UNUSED']:
            return False
        if len(self.description.strip()) == 0 or len(self.description) > 256:
            return False
        return True

    def to_dict(self):
        return {
            'position': self.position,
            'weight': self.weight,
            'description': self.description
        }

    def update_info(self, weight, description):
        self.weight = weight
        self.description = description

class Manifest:
    def __init__(self):
        self.containers = []

    def add_container(self, container):
        if container.is_valid():
            self.containers.append(container)

    def update_container(self, position, weight, description):
        for container in self.containers:
            if container.position == position:
                container.update_info(weight, description)
                return
        # If container not found, optionally add a new container
        self.add_container(Container(position, weight, description))

    def get_containers(self):
        return self.containers
